from django.urls import path
from . import views
# from .views import SongDeleteView


app_name = 'musics'

urlpatterns = [
    path('like/', views.song_like, name='like'),
    path('upload/', views.upload, name='upload'),
    path('song_upload/', views.song_upload, name='song_upload'),
    path('album_load/', views.album_upload, name='album_upload'),
    path('detail/<int:id>/<slug:slug>/', views.song_detail, name='detail'),
    path('', views.song_list, name='list'),
    path('ranking/', views.song_ranking, name='create'),
    path('song_edit/<int:id>/<slug:slug>/', views.song_edit, name='song_edit'),
    path('album/', views.album_list, name='album_list'),
    path('album_detail/<int:id>', views.album_detail, name='album_detail'),
    path('tag/<slug:tag_slug>/', views.song_list, name='song_list_by_tag'),
    path('<int:id>/delete/', views.song_delete, name='song_delete'),
    path('album_edit/<int:id>/', views.album_edit, name='album_edit'),
    path('<int:id>/album_delete/', views.album_delete, name='album_delete'),
]