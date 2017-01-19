from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
import factory

# Found the following commented lines first, but now seeing FactoryBoy might have this built in
# from PIL import Image
# import tempfile
# from django.test import override_settings

# def get_temporary_image(temp_file):
#     size = (200, 200)
#     color = (255, 0, 0, 0)
#     image = Image.new("RGBA", size, color)
#     image.save(temp_file, 'jpeg')
#     return temp_file


# class PhotoTestCase(TestCase):
#     """The Photo model test runner."""

#     @override_settings(MEDIA_ROOT=tempfile.gettempdir())
#     def test_dummy_test(self):
#             temp_file = tempfile.NamedTemporaryFile()
#             test_image = get_temporary_image(temp_file)
#             #test_image.seek(0)
#             picture = Picture.objects.create(picture=test_image.name)
#             print("It Worked!, ", picture.picture)
#             self.assertEqual(len(Picture.objects.all()), 1)


    class PhotoFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = models.Photo

            the_image = factory.django.ImageField(color='blue')


    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.photos = [self.PhotoFactory.create() for i in range(20)]


    def test_profile_is_made_when_user_is_saved(self):
        """Test that an image is saved when saved."""
        self.assertTrue(Photo.objects.count() == 20)

