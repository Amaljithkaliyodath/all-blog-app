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
]
