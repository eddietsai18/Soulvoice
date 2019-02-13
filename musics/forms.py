from django import forms
from .models import Song, Comment, Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'slug', 'album_image')


class AlbumEditForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'slug', "album_image")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('song_title', 'song_file', 'description', 'song_image', 'album', 'tags')


class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('song_title', 'description', 'tags', 'song_image', 'song_file')

