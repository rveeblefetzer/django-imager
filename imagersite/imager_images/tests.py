from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
import factory
import os
from faker import Faker

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

    def test_that_the_test_factory_works(self):
        """Test that this is happening."""
        bob = User()
        bob.username = "This Bob"
        bob.save()
        pic = Photo(author=bob)
        pic.save()
        self.assertTrue(pic.author.username == "This Bob")
