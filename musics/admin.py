from django.contrib import admin
from .models import Song, Comment, Album


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['song_title', 'song_image', 'song_file', 'created']
    list_filter = ['created']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['created', 'active', 'updated']
    search_fields = ['name', 'email', 'body']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created', 'id']
    list_filter = ['created']
