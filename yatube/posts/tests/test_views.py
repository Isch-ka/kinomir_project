from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Group

User = get_user_model()


class PostViewsTest(TestCase):
    """Тестируем view-функции приложения posts."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание группы'
        )
        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user,
            group=self.group
        )

    def test_index_page_accessible(self):
        """Проверяем доступность главной страницы."""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)

    def test_group_page_accessible(self):
        """Проверяем доступность страницы группы."""
        response = self.client.get(
            reverse('posts:group_list', args=[self.group.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_page_accessible(self):
        """Проверяем доступность страницы профайла."""
        response = self.client.get(
            reverse('posts:profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_accessible(self):
        """Проверяем доступность страницы отдельного поста."""
        response = self.client.get(
            reverse('posts:post_detail', args=[self.post.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_post_redirects_unautorized(self):
        """Проверяем: неавторизованный перенаправляется на страницу входа."""
        response = self.client.get(reverse('posts:post_create'))
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_create_post_authorized(self):
        """Проверяем: авторизованный может создать пост."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 200)


class PostSearchTest(TestCase):
    """Тестируем поиск по постам."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        Post.objects.create(
            text='Пост про утро и солнце',
            author=self.user
        )
        Post.objects.create(
            text='Вечерний пост про звёзды',
            author=self.user
        )

    def test_search_finds_matching_posts(self):
        """Проверяем, что поиск находит посты по ключевому слову."""
        response = self.client.get(reverse('posts:index'), {'q': 'утро'})
        self.assertEqual(response.status_code, 200)
        # Проверяем, что в ответе есть ключевое слово
        self.assertContains(response, 'утро')
        # Проверяем, что второй пост не отображается
        self.assertNotContains(response, 'звёзды')

    def test_search_empty_query(self):
        """Проверяем: пустой поисковый запрос показывает все посты."""
        response = self.client.get(reverse('posts:index'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пост про утро')
        self.assertContains(response, 'про звёзды')