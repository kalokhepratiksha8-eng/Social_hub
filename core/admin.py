from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follow, Story

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'caption', 'created_at']
    list_filter = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'text', 'created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at']
