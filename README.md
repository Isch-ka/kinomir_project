# Yatube - Социальная сеть для блогеров

Yatube - это платформа для публикации личных дневников, где пользователи могут создавать посты, объединять их в тематические группы и делиться своими мыслями.

## Быстрый старт

### Требования
- Python 3.9+
- Git

### Установка и запуск

1. **Клонировать репозиторий**
   ```bash
   git clone <url-вашего-репозитория>
   cd yatube_project
   ```

2. **Создать и активировать виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # для Windows (Git Bash)
   # или
   source venv/bin/activate      # для Linux/Mac
   ```

3. **Установить зависимости**
   ```bash
   pip install -r requirements.txt

   # Установка зависимостей через зеркало:
   pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com --timeout 100
   ```

4. **Выполнить миграции**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Создать суперпользователя (для доступа в админку)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Запустить сервер разработки**
   ```bash
   python manage.py runserver
   ```

7. **Открыть в браузере**
   - Сайт: http://127.0.0.1:8000/
   - Админка: http://127.0.0.1:8000/admin/

## Основные команды

| Команда | Описание |
|---------|----------|
| `python manage.py runserver` | Запуск сервера |
| `python manage.py makemigrations` | Создание миграций |
| `python manage.py migrate` | Применение миграций |
| `python manage.py createsuperuser` | Создание админа |
| `python manage.py startapp <имя>` | Создание нового приложения |

## Запуск тестов

```bash
# Запуск всех тестов
python manage.py test

# Тесты конкретного приложения
python manage.py test posts

# Конкретный файл с тестами
python manage.py test posts.tests.test_models

# Подробный вывод
python manage.py test -v 2
```

## Структура проекта

```
yatube_project/
├── yatube/              # Основная директория проекта
│   ├── posts/           # Приложение для постов
│   ├── static/          # Статические файлы (CSS, изображения)
│   ├── templates/       # HTML шаблоны
│   └── yatube/          # Настройки проекта
├── manage.py            # Утилита для управления Django
├── requirements.txt     # Зависимости проекта
└── DETAILED_README.md   # Подробная документация по созданию
```

## Основные возможности

- Просмотр ленты постов на главной странице
- Фильтрация постов по тематическим группам
- Административный интерфейс для управления контентом
- Адаптивный дизайн на Bootstrap

## Подробная документация

Полное пошаговое руководство по созданию проекта с объяснениями находится в файле [DETAILED_README.md](DETAILED_README.md).

## Лицензия

Проект распространяется под лицензией BSD 3-Clause. Подробнее в файле [LICENSE](LICENSE).
