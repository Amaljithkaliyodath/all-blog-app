# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user but don't save yet
            user.is_active = True  # Ensure the user is active
            user.save()  # Now save the user
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



