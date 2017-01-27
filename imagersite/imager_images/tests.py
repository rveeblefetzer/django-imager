from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.models import Photo, Album
import factory
import os
from faker import Faker
import datetime


fake = Faker()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_IMAGE_PATH = os.path.join(BASE_DIR, 'imager_images/test.png')


class UserFactory(factory.django.DjangoModelFactory):
    """Create a user set for testing."""

    class Meta:
        model = User
    username = factory.Sequence(lambda n: "Test user {}".format(n))


class ImageFactory(factory.django.DjangoModelFactory):
    """Create an image set for testing."""

    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "Test Image {}".format(n))
    image = SimpleUploadedFile(
        name='test.png',
        content=open(TEST_IMAGE_PATH, 'rb').read(),
        content_type='image/png'
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Create an album set for testing."""

    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "Test Album {}".format(n))


class ImageTestCase(TestCase):
    """The test runner for the Photo model."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(10)]
        self.images = [ImageFactory.build() for i in range(10)]
        self.albums = [AlbumFactory.build() for i in range(10)]
        for i in range(10):
            curr_image = self.images[i]
            curr_album = self.albums[i]
            curr_image.author = self.users[i]
            curr_album.owner = self.users[i]
            curr_image.save()
            curr_album.save()

    def test_photo_can_be_assigned_to_user(self):
        """Test that a photo and user can be connected."""
        bob = User()
        bob.username = "This Bob"
        bob.save()
        pic = Photo(author=bob)
        pic.save()
        self.assertTrue(pic.author.username == bob.username)

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
        self.assertTrue(pic.author.username == photographer.username)

    def test_album_connects_with_user(self):
        """Test that an album can be associated with a user."""
        photographer = User.objects.first()
        test_photo_set = Album(
            title="Test Photo Set",
            owner=photographer,
        )
        test_photo_set.save()
        self.assertTrue(test_photo_set.owner.username == photographer.username)

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
        pic.album = [test_photo_set]
        self.assertTrue(Photo.objects.all().get(title="test_title").title == pic.title)


class ImageFrontEndTestCase(TestCase):
    """Test Runner for the front end of the imager_images app."""

    def setUp(self):
        """Set up test users, images, and albums."""
        self.users = [UserFactory.create() for i in range(10)]
        self.images = [ImageFactory.build() for i in range(10)]
        self.albums = [AlbumFactory.build() for i in range(10)]
        for i in range(10):
            curr_image = self.images[i]
            curr_album = self.albums[i]
            curr_image.author = self.users[i]
            curr_album.owner = self.users[i]
            curr_image.save()
            curr_album.save()
        self.client = Client()
        self.request = RequestFactory()

    def test_request_images_library_page_not_logged_in(self):
        """Test that request to library page without user returns 403."""
        response = self.client.get("/images/library", follow=True)
        self.assertTrue(response.status_code == 403)

    def test_request_images_library_logged_in(self):
        """Test that request to library page with logged in user returns 200, page."""
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get("/images/library", follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'Image Library' in response.content)

    def test_request_images_library_logged_in_with_pictures(self):
        """Test that users pictures are rendered on the page."""
        user = UserFactory.create()
        self.client.force_login(user)
        photos = [ImageFactory.build() for i in range(10)]
        album = AlbumFactory.build()
        album.owner = user
        album.save()
        for photo in photos:
            photo.author = user
            photo.image = SimpleUploadedFile(
                name='test.png',
                content=open(TEST_IMAGE_PATH, 'rb').read(),
                content_type='image/png'
            )
            photo.save()
            album.pictures.add(photo)

    def test_request_photo_gallery_view_uses_correct_template(self):
        """Test that the photo gallery uses the correct template."""
        user = UserFactory.create()
        self.client.force_login(user)
        response = self.client.get("/images/photos", follow=True)
        self.assertTemplateUsed(response, "imager_images/gallery.html")

    def test_request_photo_detail_view_uses_correct_template(self):
        """Test that the photo detail view uses the correct template."""
        user = self.users[0]
        self.client.force_login(user)
        photo_id = self.images[0].id
        url = "/images/photos/" + str(photo_id)
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, "imager_images/photo_detail.html")
        self.assertTrue(b"<img src=\"/media/photos/test_" in response.content)

    def test_request_album_detail_view_renders_photo_list(self):
        """Test that the album detail view renders a list of photos."""
        user = self.users[0]
        self.client.force_login(user)
        album_id = self.albums[0].id
        url = "/images/albums/" + str(album_id)
        response = self.client.get(url, follow=True)
        self.assertTemplateUsed(response, "imager_images/album_detail.html")
        self.assertTrue(b"class=\"thumbList\"" in response.content)
