from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator  # Новый импорт
from .models import Post, Group


def index(request):
    """Главная страница Yatube с пагинацией"""
    # Получаем все посты, отсортированные по дате
    post_list = Post.objects.order_by('-pub_date')
    
    # Создаем пагинатор: 10 постов на страницу
    paginator = Paginator(post_list, 10)
    
    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page')
    
    # Получаем объекты нужной страницы
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # Передаем в шаблон объект страницы
        'total_posts': Post.objects.count(),  # Добавляем общее количество
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница с постами группы с пагинацией"""
    group = get_object_or_404(Group, slug=slug)
    
    # Получаем посты группы
    post_list = group.posts.order_by('-pub_date')
    
    # Пагинация: 10 постов на страницу
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group': group,
        'page_obj': page_obj,
        'total_posts': Post.objects.count(),  # Добавляем общее количество
    }
    return render(request, 'posts/group_list.html', context)