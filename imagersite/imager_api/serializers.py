"""Serializers for Photos for a User."""

from rest_framework import serializers
from imager_images.models import Photo, Album


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Define a serializer for the Photo object."""

    author = serializers.ReadOnlyField(source='auther.username')

    class Meta:
        model = Photo
        fields = ('title', 'description', 'date_uploaded', 'published', 'author', 'image')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    """Define serializer for album data."""
    pictures = serializers.HyperlinkedIdentityField(view_name='album_photo_list', lookup_field='pk')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Album
        fields = ('title', 'description', 'date_created', 'published', 'owner', 'album_cover', 'pictures')