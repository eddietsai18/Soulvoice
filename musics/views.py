from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SongUploadForm, CommentForm, AlbumForm, SongEditForm, AlbumEditForm
from .models import Song, Comment, Album
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import redis
from django.conf import settings
from taggit.models import Tag
from django.db.models import Q


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@login_required
def upload(request):
    return render(request,
                  'musics/music/upload.html',
                  {'section': 'upload'})


@login_required
def song_upload(request):
    if request.method == 'POST':
        form = SongUploadForm(data=request.POST,
                              files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Song added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = SongUploadForm(data=request.GET)

    return render(request,
                  'musics/music/song_upload.html',
                  {'section': 'music',
                   'form': form})


@login_required
def song_detail(request, id, slug):
    song = get_object_or_404(Song, id=id, slug=slug)
    total_views = r.incr('song:{}:views'.format(song.id))
    r.zincrby('song_ranking', song.id, 1)

    comments = song.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment (important)
            new_comment.post = song
            new_comment.save()
    else:
        comment_form = CommentForm
    return render(request,
                  'musics/music/detail.html',
                  {'song': song,
                   'total_views': total_views,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


@ajax_required
@require_POST
@login_required
def song_like(request):
    song_id = request.POST.get('id')
    action = request.POST.get('action')
    if song_id and action:
        try:
            song = Song.objects.get(id=song_id)
            if action == 'like':
                song.users_like.add(request.user)
            else:
                song.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def song_list(request, tag_slug=None):
    songs = Song.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        songs = songs.filter(tags__in=[tag])

    query = request.GET.get("q")
    if query:
        songs = songs.filter(
            Q(tags__name__icontains=query)
        ).distinct()

    paginator = Paginator(songs, 6)
    page = request.GET.get('page')
    try:
        songs = paginator.page(page)
    except PageNotAnInteger:
        songs = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        songs = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                      'musics/music/list_ajax.html',
                      {'section': 'music',
                       'songs': songs,
                       'tag': tag})
    return render(request,
                  'musics/music/list.html',
                  {'section': 'music',
                   'songs': songs,
                   'tag': tag})


@login_required
def song_ranking(request):
    song_ranking = r.zrange('song_ranking', 0, -1, desc=True)[:100]
    song_ranking_ids = [int(id) for id in song_ranking]
    most_viewed = list(Song.objects.filter(id__in=song_ranking_ids))
    most_viewed.sort(key=lambda x: song_ranking_ids.index(x.id))
    return render(request,
                  'musics/music/ranking.html',
                  {'section': 'ranking',
                   'most_viewed': most_viewed})


@login_required
def song_edit(request, id, slug):
    obj = get_object_or_404(Song, id=id, slug=slug)
    song_form = SongEditForm(data=request.POST or None,
                             files=request.FILES or None,
                             instance=obj)
    if obj.user == request.user and song_form.is_valid():
        song_form.save()
        messages.success(request, 'Song updated successfully')
        return redirect("../../../")

    return render(request, "musics/music/edit.html",
                  {"song_form": song_form,
                   "obj": obj})


@login_required
def song_delete(request, id):
    song = get_object_or_404(Song, id=id)
    if song.user == request.user and request.method == "POST":
        song.delete()
        messages.success(request, "Successfully")
        return redirect("../../")
    return render(request,
                  "musics/music/delete.html",
                  {"song": song})


@login_required
def album_list(request):
    albums = Album.objects.all()
    query = request.GET.get("q")
    if query:
        albums = albums.filter(
            Q(title__icontains=query)
        ).distinct()

    paginator = Paginator(albums, 6)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)

    except PageNotAnInteger:
        albums = paginator.page(1)

    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        albums = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,
                      'musics/album/list_ajax.html',
                      {'section': 'album',
                       'albums': albums})
    return render(request,
                  'musics/album/list.html',
                  {'section': 'album',
                   'albums': albums})


@login_required
def album_detail(request, id):
    album = get_object_or_404(Album, pk=id)
    return render(request,
                  'musics/album/detail.html',
                  {'album': album})


@login_required
def album_upload(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Album added successfully')
            return redirect(new_item.get_absolute_url())
    else:
        form = AlbumForm(data=request.GET)

    return render(request,
                  'musics/album/upload.html',
                  {'form': form})


@login_required
def album_edit(request, id):
    obj = get_object_or_404(Album, id=id)
    album_form = AlbumEditForm(data=request.POST or None,
                               files=request.FILES or None,
                               instance=obj)
    if obj.user == request.user and album_form.is_valid():
        album_form.save()
        messages.success(request, 'Album updated successfully')
        return redirect("../../album")

    return render(request, "musics/album/edit.html",
                  {"album_form": album_form,
                   "obj": obj})


@login_required
def album_delete(request, id):
    album = get_object_or_404(Album, id=id)
    if album.user == request.user and request.method == "POST":
        album.delete()
        messages.success(request, "Successfully")
        return redirect("../../album")

    return render(request,
                  "musics/album/delete.html",
                  {"song": album})