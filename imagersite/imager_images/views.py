
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

def public_gallery_view(request):
    """Display all publicly published photos."""
    photos = Photo.PublishedPhotosManager.all
    return render(request, "imager_images/gallery.html", {"photos": photos})

def photo_gallery_view(request):
    """Display the user's photo gallery view."""
    pass


def photo_detail_view(request):
    """Display the detail view for a single photo."""
    pass


def album_gallery_view(request):
    """Display the gallery view for the user."""
    pass


def album_detail_view(request):
    """Display the detail view for a specific album."""
    pass
