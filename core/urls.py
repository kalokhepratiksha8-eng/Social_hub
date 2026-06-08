from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('explore/', views.explore_view, name='explore'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/like/', views.toggle_like_view, name='toggle_like'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.toggle_follow_view, name='toggle_follow'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]
