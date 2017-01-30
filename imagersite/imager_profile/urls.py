"""URLs for the imager_profile app."""

from django.conf.urls import url

from . import views

app_name = 'imager_profile'

urlpatterns = [
    url(r'^$', views.ProfileView.as_view(), name="profile"),
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserProfileView.as_view(), name="user_profile")
]