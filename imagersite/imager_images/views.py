from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView
from imager_images.models import Album, Photo
from imager_profile.models import ImagerProfile


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


class PhotoGalleryView(ListView):
    """Define the view for the photo gallery view."""
    template_name = "imager_images/gallery.html"
    model = Photo
    queryset = Photo.published_photos.all()
    context_object_name = "photos"


class AlbumGalleryView(ListView):
    """Define the view for the photo gallery view."""
    template_name = "imager_images/albums.html"
    model = Album
    context_object_name = "albums"

    def get_queryset(self):
        """Modify get_queryset to return list of published albums for specific user."""
        return Album.published_albums.filter(owner=self.request.user)


def album_detail_view(request, pk):
    """Display the detail view for a specific album."""
    if request.user.is_authenticated():
        album = Album.objects.get(pk=pk)
        photos = album.pictures.all()
        return render(request, "imager_images/album_detail.html", {"photos": photos, "album": album})


def add_photo_view(request):
    """."""
    pass


def add_album_view(request):
    """."""
    pass
