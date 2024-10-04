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



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny  # Allow public access

class BlogPostPagination(PageNumberPagination):
    page_size = 5  # Number of blogs per page

# API view for fetching paginated blog list for all users
@api_view(['GET'])
def all_blog_posts(request):
    blogs = BlogPost.objects.all().order_by('-created_at')  # Fetch all blogs
    paginator = BlogPostPagination()
    paginated_blogs = paginator.paginate_queryset(blogs, request)
    serializer = BlogPostSerializer(paginated_blogs, many=True)
    return paginator.get_paginated_response(serializer.data)




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
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import BlogPost
# from .forms import BlogPostForm

# @login_required
# def create_blog(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             blog = form.save(commit=False)
#             blog.author = request.user
#             blog.save()
#             return redirect('my_blog')
#     else:
#         form = BlogPostForm()
#     return render(request, 'blog/create_blog.html', {'form': form})

# @login_required
# def view_blog(request, pk):
#     blog = get_object_or_404(BlogPost, pk=pk)
#     return render(request, 'blog/view_blog.html', {'blog': blog})

# @login_required
# def update_blog(request, pk):
#     blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST, instance=blog)
#         if form.is_valid():
#             form.save()
#             return redirect('my_blog')
#     else:
#         form = BlogPostForm(instance=blog)
#     return render(request, 'blog/update_blog.html', {'form': form})

# @login_required
# def delete_blog(request, pk):
#     blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
#     if request.method == 'POST':
#         blog.delete()
#         return redirect('my_blog')
#     return render(request, 'blog/delete_blog.html', {'blog': blog})

# @login_required
# def my_blog(request):
#     blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
#     return render(request, 'blog/my_blog.html', {'blogs': blogs})




from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost
from .serializers import BlogPostSerializer
from django.contrib.auth.decorators import login_required

# API view for creating a blog (POST method)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog_api(request):
    if request.method == 'POST':
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# API view for fetching the user's blogs (GET method)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_blog_api(request):
    blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    serializer = BlogPostSerializer(blogs, many=True)
    return Response(serializer.data)


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostPagination(PageNumberPagination):
    page_size = 5  # You can change this to control the number of posts per page

# API view for paginated blog list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paginated_blog_list(request):
    blogs = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    paginator = BlogPostPagination()
    paginated_blogs = paginator.paginate_queryset(blogs, request)
    serializer = BlogPostSerializer(paginated_blogs, many=True)
    return paginator.get_paginated_response(serializer.data)



# API view for fetching a single blog post by custom_id
@api_view(['GET'])
def view_single_blog(request, custom_id):
    try:
        # Remove author filtering to allow any blog to be viewed by anyone
        blog = BlogPost.objects.get(custom_id=custom_id)
    except BlogPost.DoesNotExist:
        return Response({'error': 'Blog post not found'}, status=404)
    
    serializer = BlogPostSerializer(blog)
    return Response(serializer.data)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from django.shortcuts import get_object_or_404

# API for updating a blog post (PUT method)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blog_api(request, custom_id):
    blog = get_object_or_404(BlogPost, custom_id=custom_id, author=request.user)
    serializer = BlogPostSerializer(blog, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BlogPost

# API view for deleting a blog post (DELETE method)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog_api(request, custom_id):
    blog = get_object_or_404(BlogPost, custom_id=custom_id, author=request.user)
    blog.delete()
    return Response({'message': 'Blog post deleted successfully!'}, status=204)



# Original HTML views (if needed)
@login_required
def my_blog(request):
    return render(request, 'blog/my_blog.html')

@login_required
def create_blog(request):
    return render(request, 'blog/create_blog.html')

@login_required
def view_blog(request, custom_id):
    return render(request, 'blog/view_blog.html', {'custom_id': custom_id})


from django.shortcuts import render, get_object_or_404

@login_required
def edit_blog(request, custom_id):
    blog = get_object_or_404(BlogPost, custom_id=custom_id, author=request.user)
    return render(request, 'blog/create_blog.html', {'blog': blog})



