from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class ReviewViewsTest(TestCase):
    """Тестируем view-функции приложения reviews."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='action',
            description='Напряжённые сцены'
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

    def test_index_page_accessible(self):
        """Проверяем доступность главной страницы."""
        response = self.client.get(reverse('reviews:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_shows_reviews(self):
        """Проверяем, что главная страница показывает рецензии."""
        response = self.client.get(reverse('reviews:index'))
        self.assertContains(response, 'Тестовый фильм')
        self.assertContains(response, 'Тестовый режиссёр')

    def test_genre_page_accessible(self):
        """Проверяем доступность страницы жанра."""
        response = self.client.get(
            reverse('reviews:genre_list', args=[self.genre.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_genre_page_shows_reviews(self):
        """Проверяем, что страница жанра показывает рецензии."""
        response = self.client.get(
            reverse('reviews:genre_list', args=[self.genre.slug])
        )
        self.assertContains(response, 'Тестовый фильм')

    def test_genres_list_page_accessible(self):
        """Проверяем доступность страницы списка жанров."""
        response = self.client.get(reverse('reviews:genres_list'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_accessible(self):
        """Проверяем доступность страницы профайла."""
        response = self.client.get(
            reverse('reviews:profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_page_shows_user_info(self):
        """Проверяем, что профайл показывает информацию о пользователе."""
        response = self.client.get(
            reverse('reviews:profile', args=[self.user.username])
        )
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Тестовый фильм')

    def test_review_detail_page_accessible(self):
        """Проверяем доступность страницы отдельной рецензии."""
        response = self.client.get(
            reverse('reviews:review_detail', args=[self.review.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_review_detail_page_shows_content(self):
        """Проверяем, что страница рецензии показывает полный текст."""
        response = self.client.get(
            reverse('reviews:review_detail', args=[self.review.id])
        )
        self.assertContains(response, 'Тестовый фильм')
        self.assertContains(response, 'Отличный фильм! Очень понравился.')

    def test_create_review_redirects_unauthorized(self):
        """Проверяем: неавторизованный перенаправляется на страницу входа."""
        response = self.client.get(reverse('reviews:review_create'))
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_create_review_authorized(self):
        """Проверяем: авторизованный может создать рецензию."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('reviews:review_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_review_post_success(self):
        """Проверяем: отправка формы создаёт новую рецензию."""
        self.client.force_login(self.user)
        review_count_before = Review.objects.count()
        
        response = self.client.post(
            reverse('reviews:review_create'),
            {
                'movie_title': 'Новый фильм',
                'director': 'Новый режиссёр',
                'release_year': 2023,
                'text': 'Это моя новая рецензия!',
                'rating': 9,
                'genre': self.genre.id
            }
        )
        
        review_count_after = Review.objects.count()
        self.assertEqual(review_count_after, review_count_before + 1)
        self.assertRedirects(response, reverse('reviews:profile', args=[self.user.username]))

    def test_non_approved_review_not_shown_on_index(self):
        """Проверяем: неодобренные рецензии не показываются на главной."""
        not_approved_review = Review.objects.create(
            movie_title='Скрытый фильм',
            director='Скрытый режиссёр',
            release_year=2023,
            text='Скрытая рецензия',
            rating=7,
            author=self.user,
            genre=self.genre,
            is_approved=False
        )
        
        response = self.client.get(reverse('reviews:index'))
        self.assertNotContains(response, 'Скрытый фильм')


class ReviewSearchTest(TestCase):
    """Тестируем поиск по рецензиям."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(name='Боевик', slug='action')
        
        Review.objects.create(
            movie_title='Джон Уик',
            director='Чад Стахелски',
            release_year=2014,
            text='Отличный боевик про киллера',
            rating=8,
            author=self.user,
            genre=self.genre,
            is_approved=True
        )
        Review.objects.create(
            movie_title='Оппенгеймер',
            director='Кристофер Нолан',
            release_year=2023,
            text='Глубокая драма о создателе атомной бомбы',
            rating=10,
            author=self.user,
            genre=self.genre,
            is_approved=True
        )

    def test_search_finds_matching_movies(self):
        """Проверяем, что поиск находит фильмы по названию."""
        response = self.client.get(reverse('reviews:index'), {'q': 'Джон'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Джон Уик')
        self.assertNotContains(response, 'Оппенгеймер')

    def test_search_finds_by_director(self):
        """Проверяем, что поиск находит фильмы по режиссёру."""
        response = self.client.get(reverse('reviews:index'), {'q': 'Нолан'})
        self.assertContains(response, 'Оппенгеймер')
        self.assertNotContains(response, 'Джон Уик')

    def test_search_empty_query(self):
        """Проверяем: пустой поисковый запрос показывает все рецензии."""
        response = self.client.get(reverse('reviews:index'), {'q': ''})
        self.assertContains(response, 'Джон Уик')
        self.assertContains(response, 'Оппенгеймер')

    def test_search_no_results(self):
        """Проверяем: поиск по несуществующему запросу не даёт результатов."""
        response = self.client.get(reverse('reviews:index'), {'q': 'несуществующий_фильм'})
        self.assertNotContains(response, 'Джон Уик')
        self.assertNotContains(response, 'Оппенгеймер')


class ProfileSearchTest(TestCase):
    """Тестируем поиск пользователей."""

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='alex_fan', first_name='Алексей')
        self.user2 = User.objects.create_user(username='movie_lover', first_name='Дмитрий')
        self.user3 = User.objects.create_user(username='cinema_critic', first_name='Анна')

    def test_profile_search_finds_by_username(self):
        """Проверяем поиск по username."""
        response = self.client.get(reverse('reviews:profile_search'), {'q': 'alex'})
        self.assertContains(response, 'alex_fan')
        self.assertNotContains(response, 'movie_lover')

    def test_profile_search_finds_by_first_name(self):
        """Проверяем поиск по имени."""
        response = self.client.get(reverse('reviews:profile_search'), {'q': 'Анна'})
        self.assertContains(response, 'cinema_critic')
        self.assertNotContains(response, 'alex_fan')

    def test_profile_search_empty_query(self):
        """Проверяем: пустой запрос не ломает страницу."""
        response = self.client.get(reverse('reviews:profile_search'), {'q': ''})
        self.assertEqual(response.status_code, 200)