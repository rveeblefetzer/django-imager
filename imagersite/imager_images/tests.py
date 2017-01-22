from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.models import Photo, Album
import factory
import os
from faker import Faker
import datetime
from django.db import transaction


fake = Faker()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_IMAGE_PATH = os.path.join(BASE_DIR, 'imager_images/test.png')


class ImageTestCase(TestCase):
    """The test runner for the Photo model."""
    # class PhotoFactory(factory.django.DjangoModelFactory):
    #     class Meta:
    #         model = Photo

    #     image = open(TEST_IMAGE_PATH)
    #     author =
    #     description = fake.paragraph()
    #     date_created = fake.date(pattern="%Y-%m-%d")
    #     date_modified = fake.date(pattern="%Y-%m-%d")
    #     date_published = ""
    #     published = "private"
    #     albums = ""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.new_user = User.objects.create_user("joe")

    def test_photo_can_be_assigned_to_user(self):
        """Test that a photo and user can be connected."""
        bob = User()
        bob.username = "This Bob"
        bob.save()
        pic = Photo(author=bob)
        pic.save()
        self.assertTrue(pic.author.username == "This Bob")

    def test_data_fields_can_be_filled(self):
        """Test instantiating a photo with full data fields."""
        upl_image = SimpleUploadedFile(
            name='test.png',
            content=open(TEST_IMAGE_PATH, 'rb').read(),
            content_type='image/png'
        )

        photographer = User.objects.first()
        pic = Photo(
            author=photographer,
            title="test_title",
            description="test_description",
            image=upl_image
        )
        pic.save()
        self.assertIsInstance(pic.date_uploaded, datetime.date)
        self.assertIsInstance(pic.date_modified, datetime.date)
        self.assertTrue(pic.title == "test_title")
        self.assertTrue(pic.description == "test_description")
        self.assertTrue(pic.author.username == "joe")

    def test_album_connects_with_user(self):
        """Test that an album can be associated with a user."""
        photographer = User.objects.first()
        test_photo_set = Album(
            title="Test Photo Set",
            owner=photographer,
        )
        test_photo_set.save()
        self.assertTrue(test_photo_set.owner.username == "joe")

    def test_photo_connects_with_album(self):
        """Test that a photo can be associated with an album."""
        upl_image = SimpleUploadedFile(
            name='test.png',
            content=open(TEST_IMAGE_PATH, 'rb').read(),
            content_type='image/png'
        )

        photographer = User.objects.first()
        test_photo_set = Album(
            title="Test Photo Set",
            owner=photographer,
        )
        test_photo_set.save()
        pic = Photo(
            author=photographer,
            title="test_title",
            description="test_description",
            image=upl_image,
        )
        pic.save()
        pic.albums = [test_photo_set]
        self.assertTrue(Album.objects.first().id == 2)
        self.assertTrue(Photo.objects.filter(albums__id=2).first().title == "test_title")
