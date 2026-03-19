from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Group


def index(request):
    """Главная страница Yatube с поиском по ключевым словам"""
    # Базовый запрос - все посты
    post_list = Post.objects.all().order_by('-pub_date')
    
    # Получаем поисковый запрос из GET-параметров
    query = request.GET.get('q', '')
    
    # Если есть поисковый запрос, фильтруем посты
    if query:
        post_list = post_list.filter(text__icontains=query)
    
    # Применяем select_related для оптимизации запросов
    post_list = post_list.select_related('author', 'group')
    
    # Пагинация
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_posts': Post.objects.count(),
        'query': query,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница с постами группы"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date')
    
    # Оптимизация запросов
    post_list = post_list.select_related('author')
    
    # Пагинация
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group': group,
        'page_obj': page_obj,
        'total_posts': post_list.count(),
    }
    return render(request, 'posts/group_list.html', context)