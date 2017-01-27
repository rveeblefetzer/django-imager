"""URLs for the imager_images app."""

from django.conf.urls import url
from django.views.generic import DetailView
from imager_images.models import Photo, Album
from imager_images.views import (
    library_view,
    PhotoGalleryView,
    AlbumGalleryView,
    album_detail_view,
    add_photo_view,
    add_album_view
)

app_name = 'imager_images'

urlpatterns = [
    url(r'^library/$', library_view, name="library"),
    url(r'^photos/$', PhotoGalleryView.as_view(), name="photos"),
    url(r'^photos/add/$', add_photo_view, name="add_photo"),
    url(r'^photos/(?P<pk>\d+)/$', DetailView.as_view(
        model=Photo,
        template_name="imager_images/photo_detail.html",
        context_object_name="photo"
    ), name="photo"),
    url(r'^albums/$', AlbumGalleryView.as_view(), name="albums"),
    url(r'^albums/add/$', add_album_view, name="add_album"),
    url(r'^albums/(?P<pk>\d+)/$', album_detail_view, name="album")
]
