from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user but don't save yet
            user.is_active = True  # Ensure the user is active
            user.save()  # Now save the user

            # Specify the backend being used
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)  # Log in the user immediately after signup
            messages.success(request, 'Signup successful. Welcome!')
            return redirect('index')  # Redirect to home page or dashboard after signup
        else:
            messages.error(request, 'Signup failed. Please correct the errors below.')
            print(form.errors)  # This helps to debug form errors in terminal
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/signup.html', {'form': form})





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == 'POST':
        login_identifier = request.POST.get('login')  # Could be email or username
        password = request.POST.get('password')

        # Try to authenticate with email first, fallback to username if email fails
        try:
            user_obj = get_user_model().objects.get(email=login_identifier)
            username = user_obj.username
        except get_user_model().DoesNotExist:
            username = login_identifier  # Assume it's a username if email is not found

        # Now authenticate with the found username (or login_identifier if it's a username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to index or dashboard
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'blog/login.html')













from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'blog/index.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('signup')  # Redirect to signup page


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'blog/profile.html', {'form': form})





# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('my_blog')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog.html', {'form': form})

@login_required
def view_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/view_blog.html', {'blog': blog})

@login_required
def update_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('my_blog')
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'blog/update_blog.html', {'form': form})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('my_blog')
    return render(request, 'blog/delete_blog.html', {'blog': blog})

@login_required
def my_blog(request):
    blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_blog.html', {'blogs': blogs})
