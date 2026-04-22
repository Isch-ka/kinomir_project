from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ReviewForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Review, Genre

User = get_user_model()


def index(request):
    """Главная страница КиноМир с поиском по рецензиям"""
    # Базовый запрос - только одобренные рецензии
    review_list = Review.objects.filter(is_approved=True).order_by('-pub_date')

    # Получаем поисковый запрос из GET-параметров
    query = request.GET.get('q', '')
    
    # Если есть поисковый запрос, фильтруем рецензии
    if query:
        review_list = review_list.filter(
            Q(movie_title__icontains=query) | 
            Q(director__icontains=query) |
            Q(text__icontains=query)
        )
    
    # Применяем select_related для оптимизации запросов
    review_list = review_list.select_related('author', 'genre')
    
    # Пагинация
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_reviews': Review.objects.filter(is_approved=True).count(),
        'query': query,
    }
    return render(request, 'reviews/index.html', context)


def genre_reviews(request, slug):
    """Страница с рецензиями по жанру"""
    genre = get_object_or_404(Genre, slug=slug)
    review_list = genre.reviews.filter(is_approved=True).order_by('-pub_date')

    # Оптимизация запросов
    review_list = review_list.select_related('author')
    
    # Пагинация
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'genre': genre,
        'page_obj': page_obj,
        'total_reviews': review_list.count(),
    }
    return render(request, 'reviews/genre_list.html', context)


def genres_list(request):
    """Страница со списком всех жанров"""
    genres = Genre.objects.all().order_by('name')
    
    # Добавляем количество рецензий для каждого жанра
    for genre in genres:
        genre.reviews_count = genre.reviews.filter(is_approved=True).count()
    
    paginator = Paginator(genres, 12)  # 12 жанров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_genres': Genre.objects.count(),
        'total_reviews': Review.objects.filter(is_approved=True).count(),
    }
    return render(request, 'reviews/genres_list.html', context)


def genre_search(request):
    """Поиск жанров по названию или описанию"""
    query = request.GET.get('q', '')
    genres = Genre.objects.all()
    
    if query:
        genres = genres.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by('name')
    
    # Добавляем количество рецензий для каждого жанра
    for genre in genres:
        genre.reviews_count = genre.reviews.filter(is_approved=True).count()
    
    paginator = Paginator(genres, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_genres': genres.count(),
        'query': query,
        'total_reviews': Review.objects.filter(is_approved=True).count(),
    }
    return render(request, 'reviews/genres_list.html', context)


@login_required
def review_create(request):
    """Страница создания новой рецензии"""
    form = ReviewForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        review.is_approved = request.user.is_staff  # True для админа, False для обычных
        review.save()
        print(f"✅ Рецензия создана: {review.movie_title}, is_approved={review.is_approved}")
        return redirect('reviews:profile', username=request.user.username)
    
    context = {'form': form, 'is_edit': False}
    return render(request, 'reviews/review_form.html', context)


@login_required
def review_edit(request, review_id):
    """Страница редактирования рецензии (только для автора или админа)"""
    review = get_object_or_404(Review, id=review_id)
    
    if review.author != request.user and not request.user.is_staff:
        return redirect('reviews:profile', username=request.user.username)
    
    form = ReviewForm(request.POST or None, instance=review)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('reviews:profile', username=request.user.username)
    
    context = {
        'form': form,
        'is_edit': True,
        'review_id': review_id,
    }
    return render(request, 'reviews/review_form.html', context)


@staff_member_required
def review_moderate(request, review_id):
    """Модерация рецензии (только для админов)"""
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    return redirect('reviews:review_detail', review_id=review_id)


def profile(request, username):
    """Профайл пользователя"""
    author = get_object_or_404(User, username=username)
    
    # Если смотрим свой профайл — показываем все рецензии
    # Если чужой — только одобренные
    if request.user == author:
        review_list = author.reviews.select_related('genre').order_by('-pub_date')
    else:
        review_list = author.reviews.filter(is_approved=True).select_related('genre').order_by('-pub_date')
    
    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
        'total_reviews': review_list.count(),
    }
    return render(request, 'reviews/profile.html', context)


def review_detail(request, review_id):
    """Страница отдельной рецензии"""
    review = get_object_or_404(Review, id=review_id)
    total_reviews = review.author.reviews.filter(is_approved=True).count()
    
    context = {
        'review': review,
        'total_reviews': total_reviews,
    }
    return render(request, 'reviews/review_detail.html', context)


def profile_search(request):
    """Поиск пользователей по имени или username"""
    query = request.GET.get('q', '')
    users = User.objects.all()
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).order_by('username')
    
    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'total_users': users.count(),
    }
    return render(request, 'reviews/profile_search.html', context)