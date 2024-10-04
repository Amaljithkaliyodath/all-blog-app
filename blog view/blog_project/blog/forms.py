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

# forms.py
from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full p-2 rounded-md border'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full p-2 rounded-md border'}),
        }




# forms.py
from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'rich-text-editor'}),
        }
