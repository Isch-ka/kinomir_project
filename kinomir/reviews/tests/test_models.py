from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class GenreModelTest(TestCase):
    """Тестируем модель Genre."""

    def setUp(self):
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='action',
            description='Напряжённые сцены и погони'
        )

    def test_genre_creation(self):
        """Проверяем, что жанр создаётся корректно."""
        self.assertEqual(self.genre.name, 'Боевик')
        self.assertEqual(self.genre.slug, 'action')
        self.assertEqual(self.genre.description, 'Напряжённые сцены и погони')

    def test_genre_str_method(self):
        """Проверяем строковое представление жанра."""
        self.assertEqual(str(self.genre), 'Боевик')

    def test_genre_slug_unique(self):
        """Проверяем, что slug уникален."""
        with self.assertRaises(Exception):
            Genre.objects.create(
                name='Другой боевик',
                slug='action',
                description='Описание'
            )


class ReviewModelTest(TestCase):
    """Тестируем модель Review."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
        )
        self.review = Review.objects.create(
            movie_title='Тестовый фильм',
            director='Тестовый режиссёр',
            release_year=2020,
            text='Отличный фильм! Очень понравился.',
            rating=8,
            author=self.user,
            genre=self.genre,
            is_approved=True
        )

    def test_review_creation(self):
        """Проверяем, что рецензия создаётся корректно."""
        self.assertEqual(self.review.movie_title, 'Тестовый фильм')
        self.assertEqual(self.review.director, 'Тестовый режиссёр')
        self.assertEqual(self.review.release_year, 2020)
        self.assertEqual(self.review.rating, 8)
        self.assertTrue(self.review.is_approved)
        self.assertIsNotNone(self.review.pub_date)

    def test_review_str_method(self):
        """Проверяем строковое представление рецензии."""
        expected = 'Тестовый фильм (2020) - testuser'
        self.assertEqual(str(self.review), expected)

    def test_review_rating_choices(self):
        """Проверяем, что оценка соответствует choices."""
        valid_ratings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertIn(self.review.rating, valid_ratings)

    def test_review_ordering(self):
        """Проверяем сортировку рецензий по убыванию даты."""
        review2 = Review.objects.create(
            movie_title='Новый фильм',
            director='Новый режиссёр',
            release_year=2021,
            text='Тоже хороший фильм',
            rating=9,
            author=self.user,
            genre=self.genre,
            is_approved=True
        )
        reviews = Review.objects.all()
        self.assertGreater(reviews[0].pub_date, reviews[1].pub_date)