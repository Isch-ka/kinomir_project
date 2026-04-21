from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.forms import ReviewForm
from reviews.models import Genre

User = get_user_model()


class ReviewFormTest(TestCase):
    """Тестируем форму ReviewForm."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
        )

    def test_valid_form_with_genre(self):
        """Проверяем валидную форму с жанром."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 8,
            'genre': self.genre.id
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_without_genre(self):
        """Проверяем валидную форму без жанра."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_text_invalid(self):
        """Проверяем: пустой текст рецензии не проходит валидацию."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': '',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_whitespace_text_invalid(self):
        """Проверяем: текст из пробелов не проходит валидацию."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': '   ',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_empty_movie_title_invalid(self):
        """Проверяем: пустое название фильма не проходит валидацию."""
        form_data = {
            'movie_title': '',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('movie_title', form.errors)

    def test_invalid_release_year_too_old(self):
        """Проверяем: слишком старый год выпуска."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 1800,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors)

    def test_invalid_release_year_future(self):
        """Проверяем: год выпуска в будущем."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2030,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors)

    def test_invalid_rating(self):
        """Проверяем: оценка вне диапазона 1-10."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 15
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_save_review_with_author(self):
        """Проверяем сохранение рецензии с автором."""
        form_data = {
            'movie_title': 'Новый фильм',
            'director': 'Новый режиссёр',
            'release_year': 2023,
            'text': 'Отличный фильм!',
            'rating': 9,
            'genre': self.genre.id
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        review = form.save(commit=False)
        review.author = self.user
        review.save()
        
        self.assertEqual(review.movie_title, 'Новый фильм')
        self.assertEqual(review.author, self.user)
        self.assertEqual(review.genre, self.genre)