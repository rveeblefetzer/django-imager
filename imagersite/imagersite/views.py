from django.contrib.auth.models import User
from django.conf import settings
from imager_images.models import Photo
import random
import os

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """This is the home view."""

    template_name = "imagersite/home.html"

    def get_context_data(self):
        """Get necessary data for Home view."""
        usrlist = User.objects.all()
        bg_photos = Photo.published_photos.all()
        if len(bg_photos):
            img_url = random.choice(bg_photos).image.url
        else:
            img_url = os.path.join(settings.MEDIA_URL, "photos/rainier.jpg")

        return {"usrlist": usrlist, "img_url": img_url}
