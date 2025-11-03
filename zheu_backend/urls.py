# zheu_backend/urls.py (основной файл с API)
from django.contrib import admin
from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth  # Импортируем JWTAuth здесь для глобального использования
from apps.users.api import router as users_router
from apps.paymets.api import router as payments_router

# Создаем API instance с глобальной аутентификацией
api = NinjaExtraAPI(
    title="My Backend API",
    version="1.0.0",
    description="Backend API с JWT авторизацией",
    auth=JWTAuth()  # Глобальная аутентификация для всех роутеров (кроме тех, где auth=None)
)

# Регистрируем JWT контроллер (для /token и /token/refresh)
api.register_controllers(NinjaJWTDefaultController)

# Импортируем и регистрируем роутеры из приложений

api.add_router("/users/", users_router)

api.add_router("/payments/", payments_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # Все API эндпоинты будут доступны по /api/
]