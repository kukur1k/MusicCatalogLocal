from django.shortcuts import render, get_object_or_404, redirect  # Утилиты для работы с представлениями
from django.db.models import Q  # Для сложных запросов с OR (логическое ИЛИ)
from django.contrib import messages
from .models import Musician, MusicTrack, Album
from .forms import MusicianForm, MusicTrackForm, AlbumForm, AlbumSearchForm, TrackSearchForm, MusicianSearchForm
from django.shortcuts import redirect




def home(request):

    # Подсчет количества записей в базе данных
    total_tracks = MusicTrack.objects.count()  
    total_albums = Album.objects.count()  
    recent_tracks = MusicTrack.objects.all()[:5]
    
    favorite_tracks = []
    if request.user.is_authenticated:
        # Берем треки из модели FavoriteTrack
        favorite_tracks = MusicTrack.objects.filter(
            favorited_by__user=request.user
        )[:6]  # последние 6 избранных
    else:
        favorite_tracks = []

    # Контекст для передачи в шаблон
    context = {
        'total_tracks': total_tracks,
        'total_albums': total_albums,
        'recent_tracks': recent_tracks,
        'favorite_tracks': favorite_tracks,
    }
    return render(request, 'music/home.html', context)

# ========================================Альбомы================================


def album_list(request):

    albums = Album.objects.select_related('musician').all()

    form = AlbumSearchForm(request.GET)

    if form.is_valid():
        query  = form.cleaned_data.get('query')
        musician = form.cleaned_data.get('musician')
        year_from = form.cleaned_data.get('year_from')
        year_to = form.cleaned_data.get('year_to')
        genre = form.cleaned_data.get('genre')

        if query:
            albums = albums.filter(
                Q(title__icontains=query) |
                Q(musician__name__icontains=query)
            )

        if musician:
            albums = albums.filter(musician=musician)

        if year_from and year_from is not None and year_from != '':
            albums = albums.filter(release_date__year__gte=year_from)

        if year_to and year_from is not None and year_to != '':
            albums = albums.filter(release_date__year__lte=year_from)

    context = {
        'albums': albums, 
        'form': form,   
    }
    return render(request, 'music/album_list.html', context)


def album_detail(request, pk):    
    album = get_object_or_404(Album.objects.select_related('musician'), pk=pk)
    return render(request, 'music/album_detail.html', {'album': album})


def album_create(request):
    
    if request.method == 'POST':
        # Создаем форму с переданными данными и файлами
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем книгу в БД
            album = form.save()
            # Добавляем сообщение об успехе
            messages.success(request, f'Альбом "{album.title}" успешно добавлен!')
            # Перенаправляем на страницу созданной книги
            return redirect('music:album_detail', pk=album.pk)
    else:
        # GET запрос - создаем пустую форму
        form = AlbumForm()
    
    # Рендерим шаблон с формой
    return render(request, 'music/album_form.html', {'form': form, 'title': 'Добавить альбом'})



def album_update(request, pk):


    album = get_object_or_404(Album, pk=pk)
    
    if request.method == 'POST':
        
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
           
            album = form.save()
            messages.success(request, f'Альбом "{album.title}" успешно обновлен!')
            return redirect('music:album_detail', pk=album.pk)
    else:
        form = AlbumForm(instance=album)
    
    return render(request, 'music/album_form.html', {'form': form, 'title': 'Редактировать альбом'})




def album_delete(request, pk):

    album = get_object_or_404(Album, pk=pk)
    
    if request.method == 'POST':
        
        album.delete()
        messages.success(request, f'Альбом "{album.title}" удален!')
        return redirect('music:album_list')
    
    # GET запрос - показываем страницу подтверждения
    return render(request, 'music/album_confirm_delete.html', {'album': album})



def album_detail(request, pk):    
    album = get_object_or_404(Album.objects.select_related('musician'), pk=pk)
    return render(request, 'music/album_detail.html', {'album': album})


def album_create(request):
    
    if request.method == 'POST':
        
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем книгу в БД
            album = form.save()
            # Добавляем сообщение об успехе
            messages.success(request, f'Альбом "{album.title}" успешно добавлен!')
          
            return redirect('music:album_detail', pk=album.pk)
    else:
        # GET запрос - создаем пустую форму
        form = AlbumForm()
    
    # Рендерим шаблон с формой
    return render(request, 'music/album_form.html', {'form': form, 'title': 'Добавить альбом'})



#================================Исполнители=====================================

def musician_list(request):

    musicians = Musician.objects.all()

    form = MusicianSearchForm(request.GET)

    if form.is_valid():
        query  = form.cleaned_data.get('query')
        genre = form.cleaned_data.get('genre')

        if query:
            musicians = musicians.filter(
                Q(name__icontains=query)
            )


    context = {
        'musicians': musicians, 
        'form': form,   
    }
    return render(request, 'music/musician_list.html', context)


def musician_detail(request, pk):    
    musician = get_object_or_404(Musician.objects.all(), pk=pk)
    return render(request, 'music/musician_detail.html', {'musician': musician})



def musician_delete(request, pk):

    musician = get_object_or_404(Musician, pk=pk)
    
    if request.method == 'POST':
        
        musician.delete()
        messages.success(request, f'Исполнитель "{musician.name}" удален!')
        return redirect('music:musician_list')
    
    # GET запрос - показываем страницу подтверждения
    return render(request, 'music/musician_confirm_delete.html', {'musician': musician})




def musician_create(request):
    
    if request.method == 'POST':
        
        form = MusicianForm(request.POST, request.FILES)
        if form.is_valid():
    
            musician = form.save()
         
            messages.success(request, f'Исполнитель "{musician.name}" успешно добавлен!')
          
            return redirect('music:musician_detail', pk=musician.pk)
    else:
        # GET запрос - создаем пустую форму
        form = MusicianForm()
    
    # Рендерим шаблон с формой
    return render(request, 'music/musician_form.html', {'form': form, 'title': 'Добавить исполнителя', 'musician': None})


def musician_update(request, pk):


    musician = get_object_or_404(Musician, pk=pk)
    
    if request.method == 'POST':
        
        form = MusicianForm(request.POST, request.FILES, instance=musician)
        if form.is_valid():
           
            musician = form.save()
            messages.success(request, f'Исполнитель "{musician.name}" успешно обновлен!')
            return redirect('music:musician_detail', pk=musician.pk)
    else:
        form = MusicianForm(instance=musician)
    
    return render(request, 'music/musician_form.html', 
                  {'form': form, 'title': 'Редактировать карточку исполнителя', 'musician': musician})



# ========================================Треки================================



def track_list(request):
    tracks = MusicTrack.objects.select_related('album').all()
    form = TrackSearchForm(request.GET)
    
    # Получаем ID избранных треков текущего пользователя
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = request.user.favorite_tracks.values_list('track_id', flat=True)
    
    # Фильтр "только избранное" для текущего пользователя
    favorite_only = request.GET.get('favorite') == 'only'
    if favorite_only and request.user.is_authenticated:
        tracks = tracks.filter(id__in=user_favorites)
    elif favorite_only and not request.user.is_authenticated:
        tracks = tracks.none()  # Неавторизованным показываем пустой список

    if form.is_valid():
        query = form.cleaned_data.get('query')
        musician = form.cleaned_data.get('musician')
        album = form.cleaned_data.get('album')
        release_date = form.cleaned_data.get('release_date')
        genre = form.cleaned_data.get('genre')

        if query:
            tracks = tracks.filter(
                Q(title__icontains=query) |
                Q(musician__name__icontains=query) |
                Q(album__title__icontains=query)
            )

        if musician:
            tracks = tracks.filter(musician__name__icontains=musician)
        if release_date:
            tracks = tracks.filter(release_date__year=release_date)
        if album:
            tracks = tracks.filter(album__title__icontains=album)
        if genre:
            tracks = tracks.filter(genre__name__icontains=genre)

    context = {
        'tracks': tracks,
        'form': form,
        'user_favorites': user_favorites,  # Передаем в шаблон
    }
    return render(request, 'music/track_list.html', context)




def track_detail(request, pk):    
    track = get_object_or_404(MusicTrack.objects.select_related('album', 'musician'), pk=pk)
    return render(request, 'music/track_detail.html', {'track': track})

def track_delete(request, pk):

    track = get_object_or_404(MusicTrack, pk=pk)
    
    if request.method == 'POST':
       
        track.delete()
        messages.success(request, f'Книга "{track.title}" удалена!')
        return redirect('music:album_list')
    
    # GET запрос - показываем страницу подтверждения
    return render(request, 'music/track_confirm_delete.html', {'track': track})

def track_update(request, pk):


    track = get_object_or_404(MusicTrack, pk=pk)
    
    if request.method == 'POST':
        
        form = MusicTrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
           
            track = form.save()
            messages.success(request, f'Трек "{track.title}" успешно обновлен!')
            return redirect('music:track_detail', pk=track.pk)
    else:
        form = MusicTrackForm(instance=track)
    
    return render(request, 'music/track_form.html', {'form': form, 'title': 'Редактировать трек'})


def track_create(request):
    
    if request.method == 'POST':
        
        form = MusicTrackForm(request.POST, request.FILES)
        if form.is_valid():
            
            track = form.save()
            
            messages.success(request, f'Трек "{track.title}" успешно добавлен!')
          
            return redirect('music:track_detail', pk=track.pk)
    else:
        # GET запрос - создаем пустую форму
        form = MusicTrackForm()
    
    # Рендерим шаблон с формой
    return render(request, 'music/track_form.html', {'form': form, 'title': 'Добавить трек'})


from django.contrib.auth.decorators import login_required
from .models import FavoriteTrack

@login_required
def toggle_favorite(request, track_id):
    track = get_object_or_404(MusicTrack, pk=track_id)
    favorite, created = FavoriteTrack.objects.get_or_create(
        user=request.user,
        track=track
    )
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', 'music:track_list'))



@login_required
def favorite_list(request):
    favorites = request.user.favorite_tracks.select_related('track').all()
    tracks = [fav.track for fav in favorites]
    return render(request, 'music/favorite_list.html', {'tracks': tracks})

# =======================Регистрация=====================

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('music:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})