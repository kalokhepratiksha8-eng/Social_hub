from django.urls import path
from . import api_views

urlpatterns = [
    path('posts/', api_views.PostListCreateAPI.as_view(), name='api_posts'),
    path('posts/<int:pk>/', api_views.PostDetailAPI.as_view(), name='api_post_detail'),
    path('posts/<int:post_id>/comments/', api_views.CommentListCreateAPI.as_view(), name='api_comments'),
    path('users/<str:username>/profile/', api_views.UserProfileAPI.as_view(), name='api_profile'),
    path('feed/', api_views.FeedAPI.as_view(), name='api_feed'),
]
