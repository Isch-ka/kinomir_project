from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Post, Group

User = get_user_model()


class PostFormTest(TestCase):
    """Тестируем форму PostForm."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug'
        )

    def test_valid_form_with_group(self):
        """Проверяем валидную форму с группой."""
        form_data = {
            'text': 'Текст поста',
            'group': self.group.id
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_without_group(self):
        """Проверяем валидную форму без группы."""
        form_data = {'text': 'Текст поста'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_text_invalid(self):
        """Проверяем: пустой текст поста не проходит валидацию."""
        form_data = {'text': ''}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_whitespace_text_invalid(self):
        """Проверяем: текст из пробелов не проходит валидацию."""
        form_data = {'text': '   '}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_save_post_with_author(self):
        """Проверяем сохранение поста с автором."""
        form_data = {'text': 'Новый пост', 'group': self.group.id}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        post = form.save(commit=False)
        post.author = self.user
        post.save()
        
        self.assertEqual(post.text, 'Новый пост')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group)