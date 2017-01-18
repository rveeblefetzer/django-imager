from django.shortcuts import render
from imagersite.forms import UserForm


def home_view(request):
    params = {}
    return render(request, "imagersite/home.html", params)


def register_view(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,
                  'imagersite/register.html',
                  {'user_form': user_form, 'registered': registered},
                  )
