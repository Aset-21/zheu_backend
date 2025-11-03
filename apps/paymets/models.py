# apps/payments/models.py
from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Payment(models.Model):
    date = models.DateField()
    account_number = models.CharField(max_length=50)  # № лицевого счета
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Идентификатор платежа или Номер платежа
    source = models.ForeignKey(Bank, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.account_number} - {self.amount}"