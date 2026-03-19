from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, query):
    """
    Подсвечивает все вхождения поискового запроса в тексте.
    """
    if not query or not text:
        return text
    
    # Экранируем специальные символы регулярных выражений
    escaped_query = re.escape(query)
    
    # Создаём регулярное выражение с флагом игнорирования регистра
    pattern = re.compile(f'({escaped_query})', re.IGNORECASE)
    
    # Заменяем найденные вхождения на подсвеченную версию
    highlighted = pattern.sub(
        r'<span class="highlight">\1</span>', 
        str(text)
    )
    
    return mark_safe(highlighted)


@register.filter
def highlight_limited(text, query, max_length=300):
    """
    Подсвечивает найденные слова и возвращает ограниченный фрагмент текста
    с контекстом вокруг первого вхождения.
    """
    if not query or not text:
        return text[:max_length] + ('...' if len(text) > max_length else '')
    
    text_str = str(text)
    escaped_query = re.escape(query)
    pattern = re.compile(f'({escaped_query})', re.IGNORECASE)
    
    # Находим первое вхождение запроса
    match = pattern.search(text_str)
    if not match:
        # Если запрос не найден, возвращаем начало текста
        return text_str[:max_length] + ('...' if len(text_str) > max_length else '')
    
    # Позиция первого вхождения
    start_pos = match.start()
    
    # Вычисляем начало и конец фрагмента
    context_before = 100  # символов до найденного слова
    context_after = 100   # символов после
    
    fragment_start = max(0, start_pos - context_before)
    fragment_end = min(len(text_str), start_pos + len(query) + context_after)
    
    # Вырезаем фрагмент
    fragment = text_str[fragment_start:fragment_end]
    
    # Добавляем многоточия, если нужно
    if fragment_start > 0:
        fragment = '...' + fragment
    if fragment_end < len(text_str):
        fragment = fragment + '...'
    
    # Подсвечиваем все вхождения во фрагменте
    highlighted = pattern.sub(
        r'<span class="highlight">\1</span>',
        fragment
    )
    
    return mark_safe(highlighted)