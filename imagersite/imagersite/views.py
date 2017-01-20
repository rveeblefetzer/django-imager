from django.shortcuts import render
from imagersite.forms import UserForm


def home_view(request):
    params = {}
    return render(request, "imagersite/home.html", params)
