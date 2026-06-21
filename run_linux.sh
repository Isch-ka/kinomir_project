#!/bin/bash
# Linux / Mac

if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Переход в папку проекта..."
cd kinomir

echo "Создание миграций для всех приложений..."
python manage.py makemigrations

echo "Применение миграций..."
python manage.py migrate

echo "Загрузка данных..."
python manage.py loaddata fixtures/kinomir_data.json

echo "Создание суперпользователя..."
python manage.py createsuperuser

echo "Запуск тестов..."
python manage.py test

echo "Запуск сервера..."
python manage.py runserver