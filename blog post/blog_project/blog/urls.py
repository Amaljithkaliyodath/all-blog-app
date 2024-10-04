from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import profile_view

urlpatterns = [
    path('', views.signup, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('profile/', profile_view, name='profile'),



    path('my-blog/', views.my_blog, name='my_blog'),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('view-blog/<int:pk>/', views.view_blog, name='view_blog'),
    path('update-blog/<int:pk>/', views.update_blog, name='update_blog'),
    path('delete-blog/<int:pk>/', views.delete_blog, name='delete_blog'),
    
]
