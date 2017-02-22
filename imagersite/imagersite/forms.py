from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    """Create a userform class for login."""

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        """Subclass defines form fields."""

        model = User
        fields = ('username', 'password', 'email')
