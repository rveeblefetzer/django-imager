from django.shortcuts import render

# Create your views here.


def profile_view(request):
    """Display the users profile view."""
    user = request.user
    import pdb; pdb.set_trace()
    album_list = user.owned.all()

    return render(request, "imager_profile/profile.html", {"albums": album_list})
