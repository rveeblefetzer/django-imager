"""URLs for the imager_profile app."""

from django.conf.urls import url

from . import views

app_name = 'imager_profile'

urlpatterns = [
    url(r'^$', views.profile_view, name="profile"),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_profile_view, name="user_profile")
]