from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Post, Comment, Like, Follow, Profile, Story


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name', '')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        names = full_name.split(' ', 1)
        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=names[0], last_name=names[1] if len(names) > 1 else ''
        )
        login(request, user)
        return redirect('feed')
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def feed_view(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(
        Q(author__in=following_users) | Q(author=request.user)
    ).select_related('author', 'author__profile').prefetch_related('comments', 'likes')

    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    stories_users = list(following_users) + [request.user.id]
    stories = Story.objects.filter(author__in=stories_users).select_related('author', 'author__profile').order_by('-created_at')
    seen_authors = set()
    unique_stories = []
    for story in stories:
        if story.author_id not in seen_authors and story.is_active:
            seen_authors.add(story.author_id)
            unique_stories.append(story)

    return render(request, 'feed.html', {
        'posts': posts,
        'liked_post_ids': list(liked_post_ids),
        'stories': unique_stories,
    })


@login_required
def explore_view(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).exclude(id=request.user.id)[:10]
        posts = Post.objects.filter(caption__icontains=query)[:20]
    else:
        users = []
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.exclude(author=request.user).exclude(author__in=following_users).order_by('-created_at')[:30]

    return render(request, 'explore.html', {'posts': posts, 'users': users, 'query': query})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count': posts.count(),
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profile = user.profile
        profile.bio = request.POST.get('bio', '')
        profile.website = request.POST.get('website', '')
        profile.location = request.POST.get('location', '')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile', username=user.username)
    return render(request, 'edit_profile.html')


@login_required
def create_post_view(request):
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        image = request.FILES.get('image')
        if not image:
            messages.error(request, 'Please select an image.')
            return render(request, 'create_post.html')
        Post.objects.create(author=request.user, image=image, caption=caption)
        return redirect('feed')
    return render(request, 'create_post.html')


@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('author', 'author__profile')
    is_liked = Like.objects.filter(post=post, user=request.user).exists()
    likes_count = Like.objects.filter(post=post).count()

    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        if text:
            Comment.objects.create(post=post, author=request.user, text=text)
            return redirect('post_detail', post_id=post_id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'likes_count': likes_count,
    })


@login_required
@require_POST
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('profile', username=request.user.username)


@login_required
@require_POST
def toggle_like_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    likes_count = Like.objects.filter(post=post).count()
    return JsonResponse({'liked': liked, 'likes_count': likes_count})


@login_required
@require_POST
def toggle_follow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow.delete()
        following = False
    else:
        following = True
    followers_count = Follow.objects.filter(following=target_user).count()
    return JsonResponse({'following': following, 'followers_count': followers_count})


@login_required
def notifications_view(request):
    following_me = Follow.objects.filter(following=request.user).select_related('follower', 'follower__profile').order_by('-created_at')[:20]
    my_posts = Post.objects.filter(author=request.user)
    recent_likes = Like.objects.filter(post__in=my_posts).exclude(user=request.user).select_related('user', 'user__profile', 'post').order_by('-created_at')[:20]
    recent_comments = Comment.objects.filter(post__in=my_posts).exclude(author=request.user).select_related('author', 'author__profile', 'post').order_by('-created_at')[:20]

    return render(request, 'notifications.html', {
        'following_me': following_me,
        'recent_likes': recent_likes,
        'recent_comments': recent_comments,
    })
