"""URLs for the imager_images app."""

from django.conf.urls import url
from imager_images.views import (
    LibraryView,
    PhotoGalleryView,
    AlbumGalleryView,
    AddPhotoView,
    AddAlbumView,
    EditAlbumView,
    EditPhotoView,
    ProfileTagView,
    AllPublicPhotosList,
    DetailPhotoView,
    AlbumDetailView
)

app_name = 'imager_images'

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name="library"),
    url(r'^photos/$', PhotoGalleryView.as_view(), name="photos"),
    url(r'^photos/add/$', AddPhotoView.as_view(), name="add_photo"),
    url(r'^photos/(?P<pk>\d+)/$', DetailPhotoView.as_view(), name="photo"),
    url(r'^photos/(?P<pk>\d+)/edit/$', EditPhotoView.as_view(), name="edit_photo"),
    url(r'^albums/$', AlbumGalleryView.as_view(), name="albums"),
    url(r'^albums/add/$', AddAlbumView.as_view(), name="add_album"),
    url(r'^albums/(?P<pk>\d+)/$', AlbumDetailView.as_view(), name="album"),
    url(r'^albums/(?P<pk>\d+)/edit/$', EditAlbumView.as_view(), name="edit_album"),
    url(r'^tagged/(?P<slug>[-\w]+)/$', ProfileTagView.as_view(), name="tagged_photos"),
    url(r'^public_photos/$', AllPublicPhotosList.as_view(), name='public_photos'),

]
