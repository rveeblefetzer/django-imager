from django.shortcuts import render


def home_view(request):
    params = {}
    return render(request, "imagersite/home.html", params)