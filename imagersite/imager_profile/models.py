from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class ActiveManager(models.Manager):
    """Manage the set of active users."""
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset()\
            .filter(user__is_active=True).all()


class ImagerProfile(models.Model):
    """This is the site's user profile object."""

    CAMERA_TYPES = (
        ("pinhole", "Pinhole"),
        ("fuji", "Fuji"),
        ("nikon", "Nikon"),
        ("canon", "Canon"),
        ("sony", "Sony"),
        ("hasselblad", "Hasselblad"),
        ("iphone", "iPhone"),
        ("analog slr", "analog SLR"),
        ("analog rangefinder", "analog rangefinder"),
        ("medium format", "medium format"),
        ("funsnap", "Funsnap"),
    )

    PHOTOGRAPHY_TYPE = (
        ("studio", "Studio"),
        ("portraiture", "Portraiture"),
        ("news_documentary", "News/Documentary"),
        ("street photography", "Street Photography"),
        ("weddings_events", "Weddings and Events"),
        ("erotica", "Erotica"),
        ("sports", "Sports"),
        ("product", "Product Photography"),
    )

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )
    camera_type = models.CharField(
        max_length=255,
        choices=CAMERA_TYPES,
        default="pinhole",
        null=True
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    bio = models.TextField(null=True)
    personal_website = models.URLField(max_length=200, null=True)
    hireable = models.BooleanField(default=True)
    travel_radius = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True
    )
    phone = PhoneNumberField(null=True)
    photography_type = models.CharField(
        max_length=255,
        choices=PHOTOGRAPHY_TYPE,
        default="selfies",
        null=True
    )

    active = ActiveManager()

    @property
    def is_active(self):
        """Return wether the user attached to this profile is active."""
        return self.user.is_active

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def make_profile_for_user(sender, instance, **kwargs):
    """Ensure new profile created for every user."""
    new_profile = ImagerProfile(user=instance)
    new_profile.save()
