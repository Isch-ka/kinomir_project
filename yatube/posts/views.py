from django.shortcuts import render

from .models import Post

def index(request):
    # Одна строка вместо тысячи слов на SQL:
    # в переменную posts будет сохранена выборка из 10 объектов модели Post,
    # отсортированных по полю pub_date по убыванию (от больших значений к меньшим)
    posts = Post.objects.order_by('-pub_date')[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    """Страница с постами, отфильтрованными по группам"""
    template = 'posts/group_list.html'
    # Здесь в будущем будем передавать посты группы из базы данных
    context = {
        'slug': slug,
        'group_title': 'Лев Толстой – зеркало русской революции',
        'group_description': 'Группа тайных поклонников графа.',
        'text': 'Здесь будет информация о группах проекта Yatube',
    }
    return render(request, template, context)