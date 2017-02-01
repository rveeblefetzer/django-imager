from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory
import unittest
from django.test import RequestFactory
from django.urls import reverse_lazy


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

    def test_all_profile_fields(self):
        """Test that a profile can be created with all profile fields."""
        test_user = self.users[0]
        test_user.profile.camera_type = "fuji"
        test_user.profile.address = "Some place."
        test_user.profile.bio = "Bio info here."
        test_user.profile.personal_website = "http://www.awebsite.com"
        test_user.profile.phone = "(360) 550-3355"
        test_user.profile.photography_type = "sports"
        test_user.save()
        self.assertTrue(test_user.profile.camera_type == "fuji")
        self.assertTrue(test_user.profile.address == "Some place.")
        self.assertTrue(test_user.profile.bio == "Bio info here.")
        self.assertTrue(test_user.profile.personal_website == "http://www.awebsite.com")
        self.assertTrue(test_user.profile.phone == "(360) 550-3355")
        self.assertTrue(test_user.profile.photography_type == "sports")

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
        some_guy = self.users[0]
        some_guy.is_active = False
        some_guy.save()
        self.assertTrue(ImagerProfile.active.count() == 19)


class ProfileFrontEndTests(TestCase):
    """Test the profile front end."""
    class UserFactory(factory.django.DjangoModelFactory):
        class Meta:
            model = User

        username = factory.Sequence(lambda n: "Test user {}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
        )

    def setUp(self):
        """Set up the tests."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_view_status_ok(self):
        """Test that HomeView class-based view gets 200 status code."""
        from imagersite.views import HomeView
        req = self.request.get(reverse_lazy('home'))
        view = HomeView.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

    # def test_home_route_is_status_ok(self):
    #     """I wish I knew how to say why this is the same but different from preceding."""
    #     response = self.client.get("/")
    #     self.assertTrue(response.status_code == 200)

    def test_home_route_uses_right_templates(self):
        """Test that HomeView uses expected templates."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "imagersite/home.html")
        self.assertTemplateUsed(response, "imagersite/base.html")

    def test_login_view_status(self):
        """Test that login view returns 200 status code."""
        from django.contrib.auth.views import login
        req = self.request.get(reverse_lazy('home'))
        response = login(req)
        self.assertEqual(response.status_code, 200)

    def test_login_route_uses_right_template(self):
        """Test that the login view uses expected templates."""
        response = self.client.get(reverse_lazy('login'))
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTemplateUsed(response, 'imagersite/base.html')

    def test_login_route_redirects(self):
        """Test that logging in returns user to home."""
        new_user = self.UserFactory.create()
        new_user.username = "dave"
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"
        }, follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.redirect_chain[0][0] == "/")

    def test_register_view_status(self):
        """Test register view status code is 200."""
        from registration.backends.hmac.views import RegistrationView
        req = self.request.get(reverse_lazy('home'))
        reg_view = RegistrationView.as_view()
        response = reg_view(req)
        self.assertEqual(response.status_code, 200)

    def test_can_register_new_user(self):
        """."""
        self.assertTrue(User.objects.count() == 0)
        self.client.post(
            "/accounts/register/",
            {
                "username": "joe",
                "email": "joe@joe.joe",
                "password1": "herewego",
                "password2": "herewego"
            }
        )
        self.assertTrue(User.objects.count() == 1)

    def test_registered_user_is_inactive(self):
        """Test new user is inactive."""
        self.client.post(
            "/accounts/register/",
            {
                "username": "joe",
                "email": "joe@joe.joe",
                "password1": "herewego",
                "password2": "herewego"
            }
        )
        the_user = User.objects.first()
        self.assertFalse(the_user.is_active)

    def register_joe(self, follow=False):
        """."""
        response = self.client.post(
            "/accounts/register",
            {
                "username": "joe",
                "email": "joe@joe.joe",
                "password1": "herewego",
                "password2": "herewego"
            },
            follow=follow
        )
        return response

