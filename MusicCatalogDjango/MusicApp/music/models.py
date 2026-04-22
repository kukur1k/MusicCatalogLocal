from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


class Musician(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Имя исполнителя"
    )
    country = models.CharField(
        max_length=50, 
        verbose_name="Страна исполнителя", 
        blank=True 
    )
    start_year = models.IntegerField(
        verbose_name="Начало карьеры",
        null=True,  
        blank=True 
    )

    cover_image = models.ImageField(
        upload_to='musician_covers/',  # Папка для загрузки файлов
        verbose_name="Фото исполнителя", 
        blank=True, 
        null=True  # Может быть NULL в базе данных
    )

    description = models.TextField(
        verbose_name="Об исполнителе", 
        blank=True  # Может быть пустым
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Исполнитель"  # Название в единственном числе
        verbose_name_plural = "Исполнители"  # Название во множественном числе



class Album(models.Model):
    class Genre(models.TextChoices):
        ROCK = 'rock', 'Рок'
        POP = 'pop', 'Поп'
        HIP_HOP = 'hip_hop', 'Хип-хоп'
        JAZZ = 'jazz', 'Джаз'
        CLASSICAL = 'classical', 'Классическая'
        ELECTRONIC = 'electronic', 'Электронная'
        RNB = 'rnb', 'R&B'
        FOLK = 'folk', 'Фолк'
        OTHER = 'other', 'Другое'
        METAL = 'metal', 'Метал'
        BLUES = 'blues', 'Блюз'


    title = models.CharField(
        max_length=100, 
        verbose_name="Название альбома" 
    )
    release_date = models.DateField(
        verbose_name="дата выхода",
        null=True,  
        blank=True 
    )
    cover_image = models.ImageField(
        upload_to='album_covers/',  # Папка для загрузки файлов
        verbose_name="Обложка альбома", 
        blank=True, 
        null=True  # Может быть NULL в базе данных
    )

    musician = models.ForeignKey(
        Musician, 
        on_delete=models.CASCADE,
        related_name='Albums', 
        verbose_name="Исполнитель"
    )

    genre = models.CharField(
        max_length=50, 
        verbose_name="Жанр",
        choices=Genre.choices,
        blank=True,
        null=True,
        default=Genre.OTHER
    )



    class Meta:
        verbose_name = "Альбом"  # Название в единственном числе
        verbose_name_plural = "Альбомы"  # Название во множественном числе


    def __str__(self):
        return f"{self.title} - {self.musician.name}"



class MusicTrack(models.Model):


    title = models.CharField(
        max_length=100, 
        verbose_name="Название трека" 
    )
    file = models.FileField(
        upload_to='mus_files/',  # Папка для загрузки файлов
        verbose_name="файл трека", 
        blank=True, 
        null=True  # Может быть NULL в базе данных
    )

    release_date = models.DateField(
        verbose_name="дата выхода",
        null=True,  
        blank=True 
    )

    cover_image = models.ImageField(
        upload_to='track_covers/',  # Папка для загрузки файлов
        verbose_name="Обложка трека", 
        blank=True, 
        null=True  # Может быть NULL в базе данных
    )

    is_folove = models.BooleanField(
        default=False,  # По умолчанию книга доступна
        verbose_name="В избранном"
    )

    musician = models.ForeignKey(
        Musician,
        on_delete=models.CASCADE,
        related_name='tracks', 
        verbose_name="Исполнитель"
    )

    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE,
        related_name='tracks', 
        verbose_name="Альбом"
    )

    genre = models.CharField(
        max_length=50, 
        verbose_name="Жанр",
        choices=Album.Genre.choices,
        blank=True,
        null=True,
        default=Album.Genre.OTHER
    )

    def get_cover_image(self):
        # для обложки трека
        if self.cover_image:
            return self.cover_image.url
        elif self.album and self.album.cover_image:
            return self.album.cover_image.url
        else:
            return "/static/blockPhoto.png"


    class Meta:
        verbose_name = "Трек"  # Название в единственном числе
        verbose_name_plural = "Треки"  # Название во множественном числе

    def get_absolute_url(self):
        """
        Возвращает URL для просмотра деталей трека.
        Используется в шаблонах для создания ссылок.
        """
        return reverse('track_detail', args=[str(self.id)])


    def __str__(self):
        return f"{self.title} - {self.musician.name}"




class FavoriteTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_tracks')
    track = models.ForeignKey(MusicTrack, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')  # Чтобы нельзя было добавить один трек дважды

    def __str__(self):
        return f"{self.user.username} - {self.track.title}"








