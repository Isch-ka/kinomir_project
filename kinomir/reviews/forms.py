from django import forms
from django.core.exceptions import ValidationError
from .models import Review, Genre


def validate_trailer_url(value):
    """Проверяет, что ссылка ведёт на RuTube или VK Video"""
    if value:
        allowed_domains = ['rutube.ru', 'vk.com', 'video.vk.com']
        if not any(domain in value for domain in allowed_domains):
            raise ValidationError(
                'Поддерживаются только ссылки с RuTube (rutube.ru) или VK Video (vk.com)'
            )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('movie_title', 'director', 'release_year', 'genre', 
                  'text', 'rating', 'trailer_url', 'image')
        widgets = {
            'movie_title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'movie_title': 'Название фильма',
            'director': 'Режиссёр',
            'release_year': 'Год выпуска',
            'genre': 'Жанр',
            'text': 'Ваша рецензия',
            'rating': 'Оценка',
            'trailer_url': 'Трейлер (ссылка)',
        }
        help_texts = {
            'trailer_url': 'Поддерживаются RuTube и VK Video',
            'rating': 'Оцените фильм от 1 до 10',
        }

    def clean_release_year(self):
        year = self.cleaned_data['release_year']
        current_year = 2026
        if year < 1888 or year > current_year:
            raise ValidationError(f'Год должен быть от 1888 до {current_year}')
        return year