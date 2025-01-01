from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_posts, name='get_all_posts'),  # Endpoint to get all posts
    path('create/', views.create_post, name='create_post'),  # Endpoint to create a new post
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
]