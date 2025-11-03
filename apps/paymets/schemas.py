# apps/paymets/schemas.py
from ninja import Schema, ModelSchema
from typing import Optional
from ninja.files import UploadedFile  # If needed, but likely removable; see notes
from .models import Bank  # Import the actual model class

class BankIn(Schema):
    email: str
    name: str

class BankOut(ModelSchema):
    class Config:
        model = Bank  # Use the imported class, not a string
        model_fields = ['id', 'email', 'name']

class BankUpdate(Schema):
    email: Optional[str] = None
    name: Optional[str] = None

class ParseIn(Schema):
    email: str
    # file: UploadedFile  # Remove this; file uploads are handled via function params (Form/File), not JSON schemas