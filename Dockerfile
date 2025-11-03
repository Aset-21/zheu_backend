# Используем официальный образ Python (версия 3.12, но можно изменить на вашу)
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Указываем команду запуска (используйте gunicorn для продакшена или manage.py runserver для dev)
# Для dev: python manage.py runserver 0.0.0.0:8000
# Для прод: gunicorn your_project.wsgi:application --bind 0.0.0.0:8000 (установите gunicorn в requirements.txt)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]