"""Serializers for Photos for a User."""

from rest_framework import serializers
from imager_images.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    """Define a serializer for the Photo object."""

    author = serializers.ReadOnlyField(source='auther.username')

    class Meta:
        model = Photo
        fields = ('title', 'description', 'date_uploaded', 'published', 'author', 'tags', 'image')