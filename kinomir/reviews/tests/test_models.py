from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class GenreModelTest(TestCase):
    """Тестируем модель Genre."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action',
            description='Напряжённые сцены, погони, перестрелки'
        )

    def test_verbose_name(self):
        """verbose_name в полях Genre совпадает с ожидаемым."""
        genre = GenreModelTest.genre
        field_verboses = {
            'name': 'Название жанра',
            'slug': 'Slug',
            'description': 'Описание',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    genre._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_object_name_is_name_field(self):
        """__str__ жанра - это его название."""
        genre = GenreModelTest.genre
        expected_object_name = genre.name
        self.assertEqual(expected_object_name, str(genre))


class ReviewModelTest(TestCase):
    """Тестируем модель Review."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
        )
        cls.review = Review.objects.create(
            movie_title='Тестовый фильм',
            director='Тестовый режиссёр',
            release_year=2020,
            text='Отличный фильм! Очень понравился.',
            rating=8,
            author=cls.user,
            genre=cls.genre,
            is_approved=True
        )

    def test_verbose_name(self):
        """verbose_name в полях Review совпадает с ожидаемым."""
        review = ReviewModelTest.review
        field_verboses = {
            'movie_title': 'Название фильма',
            'director': 'Режиссёр',
            'release_year': 'Год выпуска',
            'text': 'Текст рецензии',
            'rating': 'Оценка (1-10)',
            'trailer_url': 'Ссылка на трейлер',
            'is_approved': 'Одобрено администратором',
            'author': 'Автор',
            'pub_date': 'Дата публикации',
            'genre': 'Жанр',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    review._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_object_name_is_movie_title_field(self):
        """__str__ рецензии содержит название фильма, год и автора."""
        review = ReviewModelTest.review
        expected_string = f'{review.movie_title} ({review.release_year}) - {review.author.username}'
        self.assertEqual(expected_string, str(review))

    def test_rating_choices(self):
        """Оценка должна быть от 1 до 10."""
        review = ReviewModelTest.review
        valid_ratings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertIn(review.rating, valid_ratings)

    def test_review_ordering(self):
        """Рецензии сортируются по убыванию даты публикации."""
        import time
        time.sleep(0.1)

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
        reviews = Review.objects.all().order_by('-pub_date')
        self.assertGreater(reviews[0].pub_date, reviews[1].pub_date)
        
def test_review_ordering(self):
    """Рецензии сортируются по убыванию даты публикации."""
    import time
    time.sleep(0.1)  # 👈 добавь эту строку
    
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
    reviews = Review.objects.all().order_by('-pub_date')
    # Первая — review2 (новая), вторая — self.review (старая)
    self.assertGreater(reviews[0].pub_date, reviews[1].pub_date)