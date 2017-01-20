from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
import factory
import os
from django.core.file import File
from faker import Faker

fake = Faker()

# Assumes there is a test.png next to our tests.py
TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'test.png')

class PhotoFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = models.Photo

        image = factory.LazyAttribute(lambda t: File(open(TEST_IMAGE)))
        author = fake.name()
        description = fake.paragraph()
        date_created = fake.date(pattern="%Y-%m-%d")
        date_modified = fake.date(pattern="%Y-%m-%d")
        date_published = ""
        published = "private"
        albums = ""


def setUp(self):
    """The appropriate setup for the appropriate test."""
    self.photos = [self.PhotoFactory.create() for i in range(20)]


def test_that_the_test_factory_works(self):
    """Test that this is happening."""
    self.assertTrue(Photo.objects.count() == 20)

