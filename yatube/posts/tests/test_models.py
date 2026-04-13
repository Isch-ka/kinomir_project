import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):
    """Тестируем модель Post."""

    def setUp(self):
        """Создаём тестовые данные перед каждым тестом."""
        self.user = User.objects.create_user(username='testuser')
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание тестовой группы'
        )
        self.post = Post.objects.create(
            text='Тестовый текст поста',
            author=self.user,
            group=self.group
        )

    def test_post_creation(self):
        """Проверяем, что пост создаётся корректно."""
        self.assertEqual(self.post.text, 'Тестовый текст поста')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.group.title, 'Тестовая группа')
        self.assertIsNotNone(self.post.pub_date)

    def test_post_str_method(self):
        """Проверяем строковое представление поста."""
        expected = 'Тестовый текст поста'
        self.assertEqual(str(self.post), expected)

    def test_post_verbose_names(self):
        """Проверяем verbose_name полей модели."""
        field_verbose = Post._meta.get_field('text').verbose_name
        self.assertEqual(field_verbose, 'text')


class GroupModelTest(TestCase):
    """Тестируем модель Group."""

    def setUp(self):
        self.group = Group.objects.create(
            title='Группа для теста',
            slug='test-group',
            description='Описание группы'
        )

    def test_group_creation(self):
        """Проверяем, что группа создаётся корректно."""
        self.assertEqual(self.group.title, 'Группа для теста')
        self.assertEqual(self.group.slug, 'test-group')
        self.assertEqual(self.group.description, 'Описание группы')

    def test_group_str_method(self):
        """Проверяем строковое представление группы."""
        self.assertEqual(str(self.group), 'Группа для теста')