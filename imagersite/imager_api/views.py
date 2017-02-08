from django.contrib.auth.models import User
from imager_api.serializers import PhotoSerializer
from rest_framework import mixins
from rest_framework import generics


class APIUserPhotoListView(mixins.ListModelMixin, generics.GenericAPIView):
    """Class based view to return list of photos for a user."""

    serializer_class = PhotoSerializer

    def queryset(self, request):
        """Rewrite queryset to provide list of photos for single user."""
        user = User.objects.get(username=self.kwargs["username"])
        photos = user.authored.filter(published="public")
        return photos

    def get(self, request, *args, **kwargs):
        """Define get method to return list of Photo objects."""
        return self.list(request, *args, **kwargs)