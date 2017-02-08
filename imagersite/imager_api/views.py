from django.contrib.auth.models import User
from imager_images.models import Album
from imager_api.serializers import PhotoSerializer, AlbumSerializer
from rest_framework import mixins
from rest_framework import generics


class APIUserPhotoListView(mixins.ListModelMixin, generics.GenericAPIView):
    """Class based view to return list of photos for a user."""

    serializer_class = PhotoSerializer

    def get_queryset(self):
        """Rewrite queryset to provide list of photos for single user."""
        user = User.objects.get(username=self.kwargs["username"])
        photos = user.authored.filter(published="public")
        return photos

    def get(self, request, *args, **kwargs):
        """Define get method to return list of Photo objects."""
        return self.list(request, *args, **kwargs)


class APIAlbumDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Define a view to return details for a specific album."""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class APIAlbumPhotosView(mixins.ListModelMixin, generics.GenericAPIView):
    """Define a view to return a list of photos for a specific album."""
    serializer_class = PhotoSerializer

    def get_queryset(self):
        """Rewrite query set to return list of Photos for specific album."""
        return Album.objects.get(id=self.kwargs["pk"]).pictures.all()

    def get(self, request, *args, **kwargs):
        """Define get method to return list of Photos."""
        return self.list(request, *args, **kwargs)