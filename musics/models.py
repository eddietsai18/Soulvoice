from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager


class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='albums_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    album_image = models.FileField(upload_to='album_images/%Y/%m/%d', null=True, blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('musics:album_detail', args=[self.id])

    def edit_get_absolute_url(self):
        return reverse('musics:album_edit', args=[self.id])


class Song(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='songs_created',
                             on_delete=models.CASCADE)
    album = models.ForeignKey(Album,
                              related_name='album',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    song_title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    song_image = models.FileField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    song_file = models.FileField(upload_to='musics/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('musics:detail', args=[self.id, self.slug])

    def edit_get_absolute_url(self):
        return reverse('musics:song_edit', args=[self.id, self.slug])

    def __str__(self):
        return self.song_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.song_title)
        super(Song, self).save(*args, **kwargs)

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='songs_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)


class Comment(models.Model):
    post = models.ForeignKey(Song,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

