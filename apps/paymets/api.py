# apps/paymets/api.py
import os
import tempfile
from datetime import datetime, date
from ninja import Router, Form, File, Schema, Query
from ninja.files import UploadedFile
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from ninja_jwt.authentication import JWTAuth  # Импортируем правильный JWTAuth
from .models import Bank, Payment
from .schemas import BankIn, BankOut, BankUpdate, ParseIn
from .parser_exсel import ExcelPaymentParser # Assuming the file is parser_exel.py; adjust if needed
from typing import Optional, List
from pydantic import Field
from django.db.models import Q

router = Router()  # Без auth здесь — оно теперь глобальное из urls.py

@router.post("/banks")
def create_bank(request, payload: BankIn):
    bank = Bank.objects.create(**payload.dict())
    return BankOut.from_orm(bank)

@router.get("/banks", response=list[BankOut])
def list_banks(request):
    banks = Bank.objects.all()
    return [BankOut.from_orm(bank) for bank in banks]

@router.get("/banks/{bank_id}", response=BankOut)
def get_bank(request, bank_id: int):
    bank = get_object_or_404(Bank, id=bank_id)
    return BankOut.from_orm(bank)

@router.put("/banks/{bank_id}")
def update_bank(request, bank_id: int, payload: BankUpdate):
    bank = get_object_or_404(Bank, id=bank_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(bank, attr, value)
    bank.save()
    return BankOut.from_orm(bank)

@router.delete("/banks/{bank_id}")
def delete_bank(request, bank_id: int):
    bank = get_object_or_404(Bank, id=bank_id)
    bank.delete()
    return {"success": True}

@router.post("/parse")
def parse_file(request, email: str = Form(...), file: UploadedFile = File(...)):
    user = request.auth  # Теперь это работает через глобальный JWTAuth
    if not user:
        return HttpResponse("Unauthorized", status=401)

    bank = get_object_or_404(Bank, email=email)

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in file.chunks():
            tmp_file.write(chunk)
        tmp_path = tmp_file.name

    try:
        parser = ExcelPaymentParser(tmp_path)

        # Extract domain from email to determine bank (e.g., 'kazpost' from 'reports@kazpost.kz')


        # Select parser based on email domain (case-insensitive)
        if 'reports@kazpost.kz' == email:
            data = parser.extract_kazpost_data()
        elif 'imex@kaspi.kz' == email:
            data = parser.extract_kaspi_data()  # Assuming this method exists
        elif 'ensemble@halykbank.kz' == email:
            data = parser.extract_halyk_data()  # Assuming this method exists
        elif 'info@bcc.kz' == email:
            data = parser.extract_bcc_data()  # Assuming this method exists
        else:
            raise ValueError(f"No parser available for bank email: {email}")

        added_count = 0
        for item in data:
            # Parse date string to date object, handling both formats
            date_str = item['Date']
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
                except ValueError:
                    continue  # Skip invalid dates

            payment_id = item.get('PaymentID', '')

            Payment.objects.create(
                date=date_obj,
                account_number=item['Account'],
                amount=item['Amount'],
                payment_id=payment_id,
                source=bank,
                added_by=user
            )
            added_count += 1

        return {"success": True, "added_payments": added_count}
    finally:
        os.unlink(tmp_path)

class PaymentsQuery(Schema):
    bank_ids: Optional[List[int]] = Field(None)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    account_numbers: Optional[List[str]] = Field(None)
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)

@router.get("/payments")
def get_payments(request, q: PaymentsQuery = Query(...)):
    user = request.auth  # Теперь это работает через глобальный JWTAuth
    if not user:
        return HttpResponse("Unauthorized", status=401)

    queryset = Payment.objects.filter(added_by=user)

    if q.bank_ids:
        queryset = queryset.filter(source__id__in=q.bank_ids)

    if q.start_date:
        queryset = queryset.filter(date__gte=q.start_date)

    if q.end_date:
        queryset = queryset.filter(date__lte=q.end_date)

    if q.account_numbers:
        queryset = queryset.filter(account_number__in=q.account_numbers)

    total = queryset.count()
    offset = (q.page - 1) * q.page_size
    payments = queryset.order_by('-date')[offset:offset + q.page_size]

    payments_list = [
        {
            "id": p.id,
            "date": p.date.isoformat(),
            "account_number": p.account_number,
            "amount": p.amount,
            "payment_id": p.payment_id,
            "bank_id": p.source.id if p.source else None
        } for p in payments
    ]

    return {
        "payments": payments_list,
        "total": total,
        "page": q.page,
        "page_size": q.page_size,
        "total_pages": (total + q.page_size - 1) // q.page_size
    }
