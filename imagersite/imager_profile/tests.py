from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory

# Create your tests here.


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = User

        username = factory.Sequence(lambda n: "Test user {}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
        )

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [self.UserFactory.create() for i in range(20)]

    def test_profile_is_made_when_user_is_saved(self):
        """Test that an imager profile is made when user is saved."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_profile_is_associated_with_actual_users(self):
        """Test profile is associated with user objects."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, "user"))
        self.assertIsInstance(profile.user, User)

    def test_user_has_profile_attached(self):
        """Test user has profile attached."""
        user = self.users[0]
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, ImagerProfile)

    def test_profile_is_active_property(self):
        """Test the ImagerProfile is_active property."""
        user = self.users[0]
        self.assertTrue(user.profile.is_active)
        user.is_active = False
        self.assertFalse(user.profile.is_active)

    def test_profile_active_manager_returns_active_profiles(self):
        """Test the ActiveManager filters active profiles."""
        self.assertTrue(ImagerProfile.active.count() == 20)
        # some_guy = self.users[0]
        # some_guy.is_active = False
        # self.assertTrue(ImagerProfile.active.count() == 19)
