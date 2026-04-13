def truncate_text(text, max_length=30):
    """
    Обрезает текст до указанной длины и добавляет многоточие.
    """
    if not text:
        return text
    if len(text) <= max_length:
        return text
    return text[:max_length - 3].rstrip() + '...'


if __name__ == '__main__':
    # Простая ручная проверка
    print(truncate_text('Короткий текст', 30))
    print(truncate_text('Очень длинный текст, который нужно обрезать', 20))
    print(truncate_text('', 10))