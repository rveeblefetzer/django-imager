
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from imager_images.models import Album, Photo


# Create your views here.

class LibraryView(LoginRequiredMixin, TemplateView):
    """View for library."""

    template_name = "imager_images/library.html"
    login_url = reverse_lazy("login")

    def get_context_data(self):
        user = self.request.user
        album_list = user.owned.all()
        photo_list = user.authored.all()
        return {"albums": album_list, "photos": photo_list}


class PhotoGalleryView(ListView):
    """Define the view for the photo gallery view."""
    template_name = "imager_images/gallery.html"
    model = Photo
    queryset = Photo.published_photos.all()
    context_object_name = "photos"


class AlbumGalleryView(ListView):
    """Define the view for the photo gallery view."""
    template_name = "imager_images/albums.html"
    model = Album
    context_object_name = "albums"

    def get_queryset(self):
        """Modify get_queryset to return list of published albums for specific user."""
        return Album.published_albums.filter(owner=self.request.user)


class AddPhotoView(LoginRequiredMixin, CreateView):
    """Add a Photo object to the user's account."""

    login_url = reverse_lazy("login")
    template_name = "imager_images/add_photo.html"
    model = Photo
    fields = [
        "title", "description", "published", "date_published", "image",
        "tags"
    ]

    def form_valid(self, form):
        """Force the form to use the current user as the author."""
        form.instance.author = self.request.user
        photo = form.save()
        photo.author = self.request.user
        photo.save()
        return redirect("/images/library/")


class AddAlbumView(LoginRequiredMixin, CreateView):
    """Add an Album object to the User's account."""

    login_url = reverse_lazy("login")
    template_name = "imager_images/add_album.html"
    model = Album
    fields = [
        "title", "description", "album_cover", "published", "date_published", "pictures"
    ]

    def form_valid(self, form):
        """Force the form to use the current user as the author."""
        form.instance.owner = self.request.user
        album = form.save()
        album.owner = self.request.user
        album.save()
        return redirect("/images/library/")


class EditPhotoView(LoginRequiredMixin, UpdateView):
    """Define a view handler for editing photos."""

    login_url = reverse_lazy("login")
    template_name = "imager_images/edit_photo.html"
    model = Photo
    fields = [
        "title", "description", "published", "date_published", "image",
        "tags"
    ]

    def form_valid(self, form):
        """Force the form to use the current user as the author."""
        form.instance.author = self.request.user
        photo = form.save()
        photo.author = self.request.user
        photo.save()
        return redirect("/images/library/")


class EditAlbumView(LoginRequiredMixin, UpdateView):
    """Define a view handler for editing albums."""

    login_url = reverse_lazy("login")
    template_name = "imager_images/edit_album.html"
    model = Album
    fields = [
        "title", "description", "album_cover", "published", "date_published", "pictures"
    ]

    def form_valid(self, form):
        """Force the form to use the current user as the author."""
        form.instance.owner = self.request.user
        album = form.save()
        album.owner = self.request.user
        album.save()
        return redirect("/images/library/")


class ProfileTagView(ListView):
    template_name = "imager_images/profile_tag_list.html"
    slug_field_name = "tag"
    context_object_name = "photos"

    def get_queryset(self):
        return Photo.objects.filter(tags__slug=self.kwargs.get("tag")).all()

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileTagView, self).get_context_data(**kwargs)
    #     context["tag"] = self.kwargs.get("tag")
    #     return context

    def get_context_data(self):
        """Extending get_context_data method to add our data."""
        photos = Photo.objects.filter(tags__slug="tag").all()
        return {'photos': photos}