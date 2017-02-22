
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView, CreateView
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
        tag_list = Photo.tags.all()

        photo_list = user.authored.all()
        photo_paginator = Paginator(photo_list, 4)
        photo_page = self.request.GET.get('photos')

        try:
            photo_pages = photo_paginator.page(photo_page)
        except PageNotAnInteger:
            photo_pages = photo_paginator.page(1)
        except EmptyPage:
            photo_pages = photo_paginator.page(photo_paginator.num_pages)

        album_list = user.owned.all()
        album_paginator = Paginator(album_list, 4)
        album_page = self.request.GET.get('albums')

        try:
            album_pages = album_paginator.page(album_page)
        except PageNotAnInteger:
            album_pages = album_paginator.page(1)
        except EmptyPage:
            album_pages = album_paginator.page(album_paginator.num_pages)

        return {"albums": album_pages, "photos": photo_pages, "tags": tag_list}


class PhotoGalleryView(ListView):
    """Define the view for the photo gallery view."""
    template_name = "imager_images/gallery.html"
    model = Photo
    queryset = Photo.published_photos.all()
    context_object_name = "photos"
    paginate_by = 4


class AlbumGalleryView(ListView):
    """Define the view for the photo gallery view."""
    template_name = "imager_images/albums.html"
    model = Album
    context_object_name = "albums"
    paginate_by = 4

    def get_queryset(self):
        """Modify get_queryset to return list of published albums for specific user."""
        return Album.published_albums.filter(owner=self.request.user)


class DetailPhotoView(DetailView):
    """Define a view to handle the photo details."""
    model = Photo
    template_name = "imager_images/photo_detail.html"

    def get_context_data(self, **kwargs):
        """Overwrite get_context_data method to return additional info."""
        photo = Photo.objects.get(id=self.kwargs.get("pk"))
        similar_photos = Photo.published_photos.filter(
            tags__in=photo.tags.all()
        ).exclude(
            id=self.kwargs.get("pk")
        ).distinct()

        return {"similar_photos": similar_photos[:4], "photo": photo}


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


class AlbumDetailView(DetailView):
    """Define a view to handle the photo details."""
    model = Album
    template_name = "imager_images/album_detail.html"
    paginate_by = 4
    raise_exception = True

    def get_context_data(self, **kwargs):
        """Overwrite get_context_data method to return additional info."""
        album = Album.objects.get(id=self.kwargs.get("pk"))
        photos = album.pictures.all()
        tag_set = set()
        for photo in photos:
            for tag in photo.tags.all():
                tag_set.add(tag)

        photo_paginator = Paginator(photos, self.paginate_by)
        photo_page = self.request.GET.get('photo_page')

        try:
            photo_pages = photo_paginator.page(photo_page)
        except PageNotAnInteger:
            photo_pages = photo_paginator.page(1)
        except EmptyPage:
            photo_pages = photo_paginator.page(photo_paginator.num_pages)

        return {"tags": tag_set, "album": album, "photos": photo_pages}


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
    """Class-based view for user's images with specific tag."""
    template_name = "imager_images/profile_tag_list.html"
    context_object_name = "photos"

    def get_queryset(self):
        """Get tagged photos."""
        return Photo.objects.filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(ProfileTagView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context


class AllPublicPhotosList(ListView):
    """Class-based view all public photos."""
    template_name = "imager_images/public_photos.html"

    def get_queryset(self):
        """Get all public photos."""
        return Photo.objects.filter(published="public")

    def get_context_data(self):
        album_list = Album.objects.filter(published="public")
        photo_list = Photo.objects.filter(published="public")
        return {"albums": album_list, "photos": photo_list}
