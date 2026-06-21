# КиноМир — сообщество кинокритиков

## Описание проекта

**КиноМир** — это платформа для публикации рецензий на фильмы. Пользователи могут делиться мнениями о просмотренных фильмах, оценивать их, объединять рецензии по жанрам. Администратор модерирует контент перед публикацией.

## Основные возможности

- Регистрация и авторизация пользователей
- Создание, редактирование, просмотр рецензий
- Фильтрация рецензий по жанрам
- Поиск по фильмам, режиссёрам и пользователям
- Пагинация (10 рецензий на страницу)
- Модерация контента (только для администратора)
- Восстановление пароля (эмуляция через файлы)

## Технологии

- Python 3.9
- Django 4.2
- SQLite
- Bootstrap 5
- HTML/CSS

## Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone <url-репозитория>
cd kinomir_project/

# 2. Запустить скрипт развёртывания
# Windows (Git Bash):
./run_windows.sh
# Linux/Mac:
chmod +x run_linux.sh
./run_linux.sh

# Скрипт сам создаст окружение, установит зависимости, выполнит миграции и загрузит тестовые данные.

# 3. Запустить сервер
python manage.py runserver
```

## Ручной старт

```bash
# Клонировать репозиторий
git clone <url>
cd kinomir_project/

# Создать и активировать виртуальное окружение
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
source venv/bin/activate      # Linux/Mac

# Установить зависимости
pip install -r requirements.txt
# Или с зеркала
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple --trusted-host mirrors.cloud.tencent.com --timeout 100

# Выполнить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
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

## Модели данных

### Review (рецензия)
| Поле | Тип | Описание |
|------|-----|----------|
| movie_title | CharField | Название фильма |
| director | CharField | Режиссёр |
| release_year | PositiveIntegerField | Год выпуска |
| text | TextField | Текст рецензии |
| rating | IntegerField | Оценка (1-10) |
| trailer_url | URLField | Ссылка на трейлер (RuTube/VK) |
| is_approved | BooleanField | Одобрено администратором |
| author | ForeignKey | Автор рецензии |
| genre | ForeignKey | Жанр (связь с Genre) |
| pub_date | DateTimeField | Дата публикации |

### Genre (жанр)
| Поле | Тип | Описание |
|------|-----|----------|
| name | CharField | Название жанра |
| slug | SlugField | Уникальный идентификатор для URL |
| description | TextField | Описание |

## URL-маршруты

| URL | Назначение |
|-----|------------|
| `/` | Главная страница (лента рецензий) |
| `/create/` | Создание рецензии |
| `/reviews/<id>/` | Детальный просмотр рецензии |
| `/reviews/<id>/edit/` | Редактирование рецензии |
| `/reviews/<id>/moderate/` | Модерация (только админ) |
| `/profile/<username>/` | Профайл пользователя |
| `/profile/search/` | Поиск пользователей |
| `/genre/<slug>/` | Рецензии по жанру |
| `/genres/` | Список жанров |
| `/about/author/` | Об авторе |
| `/about/tech/` | Технологии |

## Ключевые компоненты кода

### Валидация формы (reviews/forms.py)

```python
class ReviewForm(forms.ModelForm):
    def clean_release_year(self):
        year = self.cleaned_data['release_year']
        if year < 1888 or year > 2026:
            raise ValidationError('Год должен быть от 1888 до 2026')
        return year
```

### Поиск с подсветкой (reviews/views.py + review_extras.py)

```python
# views.py
if query:
    review_list = review_list.filter(
        Q(movie_title__icontains=query) | 
        Q(director__icontains=query)
    )

# review_extras.py
@register.filter
def highlight(text, query):
    pattern = re.compile(f'({re.escape(query)})', re.IGNORECASE)
    return mark_safe(pattern.sub(r'<span class="highlight">\1</span>', str(text)))
```

### Декораторы

```python
@login_required
def review_create(request):
    # Только для авторизованных

@staff_member_required
def review_moderate(request, review_id):
    # Только для администратора
```

### Контекст-процессор (core/context_processors/year.py)

```python
def year(request):
    return {'year': datetime.datetime.now().year}
```

## Тестирование

```bash
# Все тесты
python manage.py test

# Только тесты приложения reviews
python manage.py test reviews

# Подробный вывод
python manage.py test -v 2

# Конкретный тестовый файл
python manage.py test reviews.tests.test_models
python manage.py test reviews.tests.test_forms
python manage.py test reviews.tests.test_views
python manage.py test reviews.tests.test_search
python manage.py test reviews.tests.test_paginator
python manage.py test reviews.tests.test_urls
```

## Coverage

Coverage (покрытие) — это инструмент, показывающий, какой процент кода покрыт тестами. Он помогает понять, какие части проекта проверены, а какие нет.
Без coverage: тесты просто проходят/падают.
С coverage: ты видишь, какие строки кода вообще не проверяются.
Нужно, чтобы убедиться, что тесты проверяют весь код, а не только его часть. Хороший показатель — 80-100%.

```bash
# Установка coverage
pip install coverage

# Запуск с покрытием (с замером покрытия)
coverage run --source='reviews,users,core,about' manage.py test -v 2

# Отчёт в консоли
coverage report

# HTML-отчёт
coverage html

# Открыть отчёт в браузере (Windows)
start htmlcov/index.html
```

## Лицензия

BSD 3-Clause