
from django.http import HttpResponseForbidden
from django.shortcuts import render
from imager_images.models import Album, Photo
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.


def library_view(request):
    """Display the library view for the user."""
    if request.user.is_authenticated():
        user = request.user
        album_list = user.owned.all()
        photo_list = user.authored.all()
        return render(
            request,
            "imager_images/library.html",
            {
                "albums": album_list,
                "photos": photo_list
            }
        )
    return HttpResponseForbidden()


def photo_gallery_view(request):
    """Display the user's photo gallery view."""
    if request.user.is_authenticated():
        photos = Photo.published_photos.all
        return render(request, "imager_images/gallery.html", {"photos": photos})
    return HttpResponseForbidden()


def photo_detail_view(request, pk):
    """Display the detail view for a single photo."""
    if request.user.is_authenticated():
        photo = Photo.objects.get(pk=pk)
        return render(request, "imager_images/photo_detail.html", {"photo": photo})


def album_gallery_view(request):
    """Display the gallery view for the user."""
    if request.user.is_authenticated():
        albums = Album.published_albums.filter(owner=request.user)
        return render(request, "imager_images/albums.html", {"albums": albums})


def album_detail_view(request, pk):
    """Display the detail view for a specific album."""
    if request.user.is_authenticated():
        album = Album.objects.get(pk=pk)
        photos = album.pictures.all()
        return render(request, "imager_images/album_detail.html", {"photos": photos, "album": album})
