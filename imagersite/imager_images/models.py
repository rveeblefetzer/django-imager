from django.db import models
from django.contrib.auth.models import User

PUBLISH_STATE = (
    ("private", "Private"),
    ("shared", "Shared"),
    ("public", "Public"),
)

class Album(models.Model):
    """The site's object for user photo albums."""
    objects = models.Manager()

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    description = models.TextField(null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)

    published = models.CharField(
        max_length=255,
        choices=PUBLISH_STATE,
        default="private",
        null=True
    )
    owner = models.ForeignKey(
        User,
        related_name="owned",
    )
    album_cover = models.FilePathField(path="/photos")


class Photo(models.Model):
    """This is the site's photo object."""
    objects = models.Manager()

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    description = models.TextField(null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)

    published = models.CharField(
        max_length=255,
        choices=PUBLISH_STATE,
        default="private",
        null=True
    )
    author = models.ForeignKey(
        User,
        related_name="authored",
    )
    albums = models.ManyToManyField(Album)
    image = models.ImageField(upload_to="photos")


