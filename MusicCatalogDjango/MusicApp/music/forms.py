from django import forms
from .models import Musician, MusicTrack, Album

# Форма для создания и редактирования исполнителей
class MusicianForm(forms.ModelForm):
    """
    Форма для работы с моделью Musician.
    Позволяет создавать и редактировать записи об авторах.
    """
    class Meta:
        model = Musician
        
        fields = ['cover_image', 'name', 'start_year', 'country', 'description']
        
        widgets = {
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя исполнителя'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',  # CSS класс Bootstrap
                'placeholder': 'Имя исполнителя'  # Подсказка в поле ввода
            }),
            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год рождения'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Страна'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Об исполнителе'
            }),
        }

# Форма для создания и редактирования альбомов
class AlbumForm(forms.ModelForm):
    """
    Форма для работы с моделью Album.
    Позволяет создавать и редактировать записи об авторах.
    """
    class Meta:
        model = Album
        
        fields = ['title', 'musician', 'genre' ,'release_date', 'cover_image']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название альбома'
            }),
            'musician': forms.Select(attrs={
                'class': 'form-control'
            }),
            'release_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата релиза (Y-M-D)',
                'type': 'date'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jбложка альбома'
            }),
            'genre': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class MusicTrackForm(forms.ModelForm):
    """
    Форма для работы с моделью Album.
    Позволяет создавать и редактировать записи об авторах.
    """
    class Meta:
        model = MusicTrack
        
        fields = ['title', 'musician', 'album', 'release_date', 'genre', 'file', 'cover_image']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название трека'
            }),
            'musician': forms.Select(attrs={
                'class': 'form-control',
            }),
            'album': forms.Select(attrs={
                'class': 'form-control',
            }),
            'release_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата релиза (Y-M-D)',
                'type': 'date'
            }),
            'genre': forms.Select(attrs={ 
                'class': 'form-control',
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Аудиофайл'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Обложка трека'
            }),
        }


# Форма для поиска треков
class TrackSearchForm(forms.Form):
    """
    Форма для фильтрации и поиска треков.
    Используется на странице каталога или поиска.
    """
    # Поиск по названию (текстовое поле)
    query = forms.CharField(
        required=False,  # Поле необязательное для заполнения
        label='Название',  # Метка поля в шаблоне
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или исполнителю'
        })
    )
    
    musician = forms.ModelChoiceField(
        queryset=Musician.objects.all(), 
        required=False,
        label='Автор',
        empty_label="Все исполнители",  # Значение по умолчанию
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Фильтр по году (начало диапазона)
    year_from = forms.IntegerField(
        required=False,
        label='Год с',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Год с'
        })
    )
    
    # Фильтр по году (конец диапазона)
    year_to = forms.IntegerField(
        required=False,
        label='Год по',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Год по'
        })
    )
    
    # Фильтр только доступных книг (чекбокс)
    folove_only = forms.BooleanField(
        required=False,
        label='Только избранное',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )





# Форма для поиска треков
class MusicianSearchForm(forms.Form):
    
    # Поиск по названию (текстовое поле)
    query = forms.CharField(
        required=False,  # Поле необязательное для заполнения
        label='Имя',  # Метка поля в шаблоне
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по имени'
        })
    )
    







# Форма для поиска треков
class AlbumSearchForm(forms.Form):
    """
    Форма для фильтрации и поиска альбомов.
    Используется на странице каталога или поиска.
    """
    # Поиск по названию (текстовое поле)
    query = forms.CharField(
        required=False,  # Поле необязательное для заполнения
        label='Название',  # Метка поля в шаблоне
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию или исполнителю'
        })
    )
    
    musician = forms.ModelChoiceField(
        queryset=Musician.objects.all(), 
        required=False,
        label='Автор',
        empty_label="Все исполнители",  # Значение по умолчанию
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Фильтр по году (начало диапазона)
    year_from = forms.IntegerField(
        required=False,
        label='Год с',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Год с'
        })
    )
    
    # Фильтр по году (конец диапазона)
    year_to = forms.IntegerField(
        required=False,
        label='Год по',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Год по'
        })
    )

    genre = forms.ChoiceField(
        choices=[('', 'Все жанры')] + Album.Genre.choices,
        required=False,
        label='Жанр',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
