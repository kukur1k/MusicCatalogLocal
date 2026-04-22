from django.urls import path

from . import views # Импорт представлений из текущего приложения

from django.contrib.auth import views as auth_views

# Пространство имен для URL-шаблонов приложения

app_name = 'music'

# Список всех URL-маршрутов приложения
urlpatterns = [
    # Главная
    path('', views.home, name='home'),
    path('albums/', views.album_list, name='album_list'),
    path('tracks/', views.track_list, name='track_list'),
    path('musicians/', views.musician_list, name='musician_list'),

    # Альбомы
    path('albums/<int:pk>/', views.album_detail, name='album_detail'),
    path('albums/create/', views.album_create, name='album_create'),
    path('albums/<int:pk>/update/', views.album_update, name='album_update'),
    path('albums/<int:pk>/delete/', views.album_delete, name='album_delete'),

    # Треки
    path('tracks/<int:pk>/', views.track_detail, name='track_detail'),
    path('tracks/create/', views.track_create, name='track_create'),
    path('tracks/<int:pk>/update/', views.track_update, name='track_update'),
    path('tracks/<int:pk>/delete/', views.track_delete, name='track_delete'),

    path('musicians/<int:pk>/', views.musician_detail, name='musician_detail'),
    path('musicians/create/', views.musician_create, name='musician_create'),
    path('musicians/<int:pk>/update/', views.musician_update, name='musician_update'),
    path('musicians/<int:pk>/delete/', views.musician_delete, name='musician_delete'),

    path('tracks/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    path('favorites/', views.favorite_list, name='favorite_list'),
    path('track/<int:track_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]

    
   