from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.db import models
from django.db.models import Count
from django.utils import timezone
from .models import Forum, Post
from .forms import ForumForm, PostForm
from user.models import User


def index(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'date_created')
    forums = Forum.objects.all()

    if query:
        forums = forums.filter(user__username__icontains=query) | forums.filter(title__icontains=query) | forums.filter(description__icontains=query)

    if sort_by == 'date_created':
        forums = forums.order_by('-created_on')
    elif sort_by == 'oldest_date_created':
        forums = forums.order_by('created_on')
    elif sort_by == 'top_day':
        forums = forums.annotate(
            num_posts=Count('post', filter=models.Q(post__posted_on__gte=timezone.now() - timezone.timedelta(days=1))))
        forums = forums.order_by('-num_posts', '-created_on')
    elif sort_by == 'top_month':
        forums = forums.annotate(
            num_posts=Count('post', filter=models.Q(post__posted_on__gte=timezone.now() - timezone.timedelta(days=30))))
        forums = forums.order_by('-num_posts', '-created_on')
    elif sort_by == 'top_year':
        forums = forums.annotate(num_posts=Count('post', filter=models.Q(
            post__posted_on__gte=timezone.now() - timezone.timedelta(days=365))))
        forums = forums.order_by('-num_posts', '-created_on')
    elif sort_by == 'num_posts':
        forums = forums.annotate(num_posts=Count('post')).order_by('-num_posts', '-created_on')

    return render(request, 'forum.html', {'forums': forums, 'search_query': query, 'sort_by': sort_by})


def create_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            if 'curr_user' in request.session:
                forum = form.save(commit=False)
                forum.user = User.objects.get(username=request.session['curr_user'])
                forum.save()
                messages.success(request, 'Forum created successfully!')
                return redirect('forum:main')
            else:
                messages.error(request, 'You need to be logged in to create a forum.')
                return redirect('forum:main')
    else:
        form = ForumForm()

    return render(request, 'create_forum.html', {'form': form})


def forum_details(request, forum_id):
    query = request.GET.get('q')
    forum = get_object_or_404(Forum, pk=forum_id)
    posts = Post.objects.filter(forum=forum)

    sort_by = request.GET.get('sort_by', 'date_created')

    if query:
        posts = posts.filter(user__username__icontains=query) | posts.filter(content__icontains=query)

    if sort_by == 'date_created':
        posts = posts.order_by('-posted_on')
    elif sort_by == 'oldest_date_created':
        posts = posts.order_by('posted_on')

    user_is_creator = False

    if 'curr_user' in request.session:
        current_user_username = request.session['curr_user']
        current_user = User.objects.filter(username=current_user_username).first()

        if current_user and current_user == forum.user:
            user_is_creator = True

    return render(request, 'forum_details.html', {'forum': forum, 'posts': posts, 'user_is_creator': user_is_creator, 'search_query': query, 'sort_by': sort_by})


def update_forum(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            form = ForumForm(request.POST, instance=forum)
            if form.is_valid():
                form.save()
                messages.success(request, 'Forum details updated successfully!')
                forum.update_forum_stats()
                return redirect('forum:forum_details', forum_id=forum_id)
        elif action == 'delete':
            forum.delete()
            messages.success(request, 'Forum deleted successfully!')
            return redirect('forum:main')
        elif action == 'cancel':
            return redirect('forum:forum_details', forum_id=forum_id)
    else:
        form = ForumForm(instance=forum)

    return render(request, 'update_forum.html', {'forum': forum, 'form': form})


def create_post(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    if request.method == 'POST':
        form = PostForm(request.POST)

        current_user = "Anonymous"
        if 'curr_user' in request.session:
            current_user_username = request.session['curr_user']
            current_user = User.objects.filter(username=current_user_username).first()

        if form.is_valid():
            post = form.save(commit=False)
            post.forum = forum
            post.user = current_user
            post.save()

            forum.update_forum_stats()

            return redirect('forum:forum_details', forum_id=forum_id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form, 'forum': forum})


class UpdatePostView(View):
    template_name = 'update_post.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
        return render(request, self.template_name, {'form': form, 'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(request.POST, instance=post)
        action = request.POST.get('action')

        if action == 'delete_post':
            forum = get_object_or_404(Forum, pk=post.forum_id)
            post.delete()
            messages.success(request, 'Post deleted successfully.')
            forum.update_forum_stats()
            return redirect('forum:forum_details', forum_id=post.forum.pk)

        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('forum:forum_details', forum_id=post.forum.pk)

        return render(request, self.template_name, {'form': form, 'post': post})