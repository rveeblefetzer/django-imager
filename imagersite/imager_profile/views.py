from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo
# Create your views here.


def profile_view(request):
    """Display the users profile view."""
    user = request.user
    album_list = user.owned.all()

    return render(request, "imager_profile/profile.html", {"albums": album_list})


def user_profile_view(request):
    """Display profile view for any user."""

    return render(request, "imager_profile/user_profile.html")