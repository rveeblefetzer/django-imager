from django.conf.urls import url

from imager_api.views import APIUserPhotoListView

app_name = 'imager_api'

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', APIUserPhotoListView.as_view(), name="api_user_photo_list"),
]