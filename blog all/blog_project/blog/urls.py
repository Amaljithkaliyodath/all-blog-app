from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import profile_view
from .views import create_blog_api, my_blog_api, my_blog, create_blog
from .views import my_blog, view_blog, paginated_blog_list, view_single_blog
from .views import my_blog, view_blog, edit_blog, paginated_blog_list, view_single_blog, update_blog_api, delete_blog_api
from .views import all_blog_posts
urlpatterns = [
    path('', views.signup, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('profile/', profile_view, name='profile'),



 

    path('create-blog/', create_blog, name='create_blog'),
    path('my-blog/', my_blog, name='my_blog'),
    path('view-blog/<str:custom_id>/', view_blog, name='view_blog'),
    path('edit-blog/<str:custom_id>/', edit_blog, name='edit_blog'),

    # API endpoints
    path('api/create-blog/', create_blog_api, name='create_blog_api'),
    path('api/my-blog/', my_blog_api, name='my_blog_api'),
    path('api/paginated-blog-list/', paginated_blog_list, name='paginated_blog_list'),
    path('api/view-blog/<str:custom_id>/', view_single_blog, name='view_single_blog'),
    path('api/update-blog/<str:custom_id>/', update_blog_api, name='update_blog_api'),
    path('api/delete-blog/<str:custom_id>/', delete_blog_api, name='delete_blog_api'),
    path('api/all-blog-posts/', all_blog_posts, name='all_blog_posts'), 
    path('view-blog/<str:custom_id>/', view_blog, name='view_blog'), 
]






    

   