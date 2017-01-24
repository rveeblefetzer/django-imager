from django.db import models
from django.contrib.auth.models import User


PUBLISH_STATE = (
    ("private", "Private"),
    ("shared", "Shared"),
    ("public", "Public"),
)


class PublishedPhotosManager(models.Manager):
    """Manage the set of published photos."""

    def get_queryset(self):
        """Return only those images that are published."""
        return super(PublishedPhotosManager, self).get_queryset()\
            .filter(published="public").all()


class Photo(models.Model):
    """This is the site's photo object."""

    objects = models.Manager()
    published_photos = PublishedPhotosManager()

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

    image = models.ImageField(upload_to="photos")

    def __str__(self):
        """Return title."""
        return self.title


class PublishedAlbumsManager(models.Manager):
    """Manage the set of public albums."""

    def get_queryset(self):
        """Return only the public albums."""
        return super(PublishedAlbumsManager, self).get_queryset()\
            .filter(published="public").all()


class Album(models.Model):
    """The site's object for user photo albums."""

    objects = models.Manager()
    published_albums = PublishedAlbumsManager()

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
    album_cover = models.ForeignKey(
        Photo,
        related_name="+",
        blank=True,
        null=True
    )
    pictures = models.ManyToManyField(
        Photo,
        related_name="album",
        blank=True,
    )

    def __str__(self):
        """Return title."""
        return self.title
