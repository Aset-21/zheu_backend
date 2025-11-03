from ninja import Schema
from datetime import datetime

# Схема для ответа с данными пользователя
class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    date_joined: datetime

# Схема для регистрации нового пользователя
class UserCreateSchema(Schema):
    username: str
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""

# Схема для сообщений об успехе/ошибке
class MessageSchema(Schema):
    message: str
