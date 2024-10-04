# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Ensure email is mandatory

    class Meta:
        model = get_user_model()  # This should point to the correct user model
        fields = ['email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)  # Save without committing
        user.email = self.cleaned_data['email']  # Ensure the email is saved
        if commit:
            user.save()  # Commit the save
        return user
