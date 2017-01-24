from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from imager_profile.models import ImagerProfile
from imager_images.models import Album, Photo
import random
import os



def home_view(request):
    usrlist = User.objects.all()
    bg_photos = Photo.published_photos.all()
    if len(bg_photos):
        img_url = random.choice(bg_photos).image.url
    else:
        img_url = os.path.join(settings.MEDIA_URL, "photos/rainier.jpg")

    return render(request, "imagersite/home.html", {"usrlist": usrlist, "img_url": img_url})
