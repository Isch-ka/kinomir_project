# КиноМир

КиноМир - сообщество киноманов

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

# Запуск тестов приложения reviews
python manage.py test reviews

# Запуск с подробным выводом
python manage.py test -v 2

# Запуск конкретного тестового файла
python manage.py test reviews.tests.test_models
python manage.py test reviews.tests.test_forms
python manage.py test reviews.tests.test_views
```

## Структура проекта

```
kinomir_project/
├── kinomir/
│   ├── reviews/          # Рецензии и жанры
│   ├── users/            # Регистрация/авторизация
│   ├── core/             # Общие компоненты
│   ├── about/            # Статические страницы
│   ├── static/           # CSS, изображения
│   ├── templates/        # HTML шаблоны
│   └── kinomir/          # Настройки проекта
├── manage.py
└── requirements.txt
```

## Лицензия

Проект распространяется под лицензией BSD 3-Clause. Подробнее в файле [LICENSE](LICENSE).