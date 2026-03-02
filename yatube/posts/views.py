from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    """Главная страница Yatube"""
    return HttpResponse(
        '<h1>Главная страница Yatube</h1>'
        '<p>Добро пожаловать в нашу уютную социальную сеть!</p>'
        '<p>Здесь вы найдете:</p>'
        '<ul>'
        '<li>Интересные посты от пользователей</li>'
        '<li>Сообщества по интересам</li>'
        '<li>Много общения и полезной информации</li>'
        '</ul>'
        '<p><a href="/group/funny-cats/">Посмотреть посты про смешных котов</a></p>'
        '<p><a href="/group/programming/">Зайти в сообщество программистов</a></p>'
    )

def group_posts(request, slug):
    """Страница с постами, отфильтрованными по группам"""
    return HttpResponse(
        f'<h1>Сообщество: {slug}</h1>'
        f'<p>Вы находитесь в группе <strong>"{slug}"</strong></p>'
        f'<p>Здесь будут отображаться посты, относящиеся к этому сообществу.</p>'
        f'<h2>Последние посты в группе:</h2>'
        f'<ul>'
        f'<li>Пост №1: "Как я вступил в группу {slug}"</li>'
        f'<li>Пост №2: "10 причин любить группу {slug}"</li>'
        f'<li>Пост №3: "Мой первый пост в {slug}"</li>'
        f'</ul>'
        f'<p><a href="/">Вернуться на главную</a></p>'
    )