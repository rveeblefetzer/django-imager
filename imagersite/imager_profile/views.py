from django.urls import reverse_lazy
from imager_profile.models import ImagerProfile
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class ProfileView(LoginRequiredMixin, DetailView):
    """Display user's profile."""

    template_name = "imager_profile/profile.html"
    model = ImagerProfile
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        """Get object from request rather than pk or slug."""
        user = request.user
        return self.render_to_response({'user': user})


class UserProfileView(DetailView):
    """Display any user's profile."""

    template_name = "imager_profile/user_profile.html"
    model = ImagerProfile
    slug_field = "user__username"
    slug_url_kwarg = "user__username"
    context_object_name = "user"
