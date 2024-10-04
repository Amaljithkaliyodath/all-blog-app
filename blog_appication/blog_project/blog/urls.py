from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('profile/', views.profile_view, name='profile'),  # Profile management page
    path('logout/', views.logout_view, name='logout'),  # Logout page
]
