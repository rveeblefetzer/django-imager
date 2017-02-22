from django.conf.urls import url

from imager_api.views import (
    APIUserPhotoListView,
    APIUserAlbumListView,
    APIAlbumPhotosView
)

app_name = 'imager_api'

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', APIUserPhotoListView.as_view(), name="api_user_photo_list"),
    url(r'^(?P<username>[\w.@+-]+)/album/$', APIUserAlbumListView.as_view(), name="api_user_album_list"),
    url(r'^album/(?P<pk>\d+)/photos/$', APIAlbumPhotosView.as_view(), name="api_album_photos"),
]