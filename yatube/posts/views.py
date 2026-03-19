from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Group


def index(request):
    """Главная страница Yatube"""
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Для главной показываем общее количество постов
    context = {
        'page_obj': page_obj,
        'total_posts': Post.objects.count(),
        'page_title': 'Главная страница',  # Добавили для контекста
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница с постами группы"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Для группы показываем количество постов ТОЛЬКО в этой группе
    context = {
        'group': group,
        'page_obj': page_obj,
        'total_posts': post_list.count(),  # Здесь считаем посты только этой группы
        'page_title': f'Группа: {group.title}',
    }
    return render(request, 'posts/group_list.html', context)