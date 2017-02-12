"""Serializers for Photos for a User."""

from rest_framework import serializers
from imager_images.models import Photo, Album


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Define a serializer for the Photo object."""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Photo
        fields = ('title', 'description', 'date_uploaded', 'published', 'author', 'image')


class AlbumSerializer(serializers.Serializer):
    """Define serializer for album data."""

    owner = serializers.ReadOnlyField(source='owner.username')
    pictures = PhotoSerializer(many=True)

    class Meta:
        model = Album
        fields = ('title', 'description', 'date_created', 'published', 'owner', 'album_cover', 'pictures')
