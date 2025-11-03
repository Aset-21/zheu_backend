from django.contrib.auth import get_user_model
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from .schemas import UserSchema, UserCreateSchema, MessageSchema


# Создаем роутер для пользовательских эндпоинтов
router = Router(tags=['Пользователи'])

User = get_user_model()


@router.post("/register", response={201: UserSchema, 400: MessageSchema})
def register(request, data: UserCreateSchema):
    """
    Регистрация нового пользователя.
    Этот эндпоинт доступен без авторизации.
    """
    # Проверка уникальности username
    if User.objects.filter(username=data.username).exists():
        return 400, {"message": "Пользователь с таким именем уже существует"}

    # Проверка уникальности email
    if User.objects.filter(email=data.email).exists():
        return 400, {"message": "Пользователь с таким email уже существует"}

    # Создание пользователя
    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )

    return 201, user


@router.get("/me", response=UserSchema, auth=JWTAuth())
def get_current_user(request):
    """
    Получение информации о текущем авторизованном пользователе.
    Требует JWT токен в заголовке: Authorization: Bearer <token>
    """
    return request.auth


@router.get("/list", response=list[UserSchema], auth=JWTAuth())
def list_users(request):
    """
    Получение списка всех пользователей (защищенный эндпоинт).
    Требует JWT токен.
    """
    users = User.objects.all()
    return users
