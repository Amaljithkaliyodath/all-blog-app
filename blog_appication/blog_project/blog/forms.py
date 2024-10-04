from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email/Username")



# blog/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Form to update the user information (username, email)
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# Form to update profile information (like profile picture)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']  # Assuming the Profile model has an 'image' field for profile pictures


