from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.views.generic import ListView

from .forms import *
from .models import *


class PostListView(ListView):
    queryset = Post.objects.order_by('-id')
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'app1/base.html'


def contacts(request):
    return render(request, 'app1/contacts.html')


def about(request):
    return render(request, 'app1/about.html')


@login_required
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'app1/create_post.html', {'form': form})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()
            login(request)
            return redirect('name')
    else:
        form = UserRegistrationForm()
    return render(request, 'app1/registration.html', {'form': form})


@login_required
@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('my_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'app1/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('name')

    return render(request, 'app1/login.html')


def logout_user(request):
    logout(request)
    return redirect('base')


@login_required
def name(request):
    return render(request, 'app1/name.html')


@login_required
@csrf_exempt
def user_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id, author=request.user)
        if post.author == request.user:
            post.delete()
            return redirect('user_post')
    posts = Post.objects.filter(author=request.user).order_by('-id')
    context = {'posts': posts}
    return render(request, 'app1/user_post.html', context)


@login_required
@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, 'Произошла ошибка!')
        return redirect('user_post')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('user_post')
    else:
        form = PostForm(instance=post)

    return render(request, 'app1/edit_post.html', {'form': form})


@login_required
@csrf_exempt
def home(request):
    posts = Post.objects.order_by('-id')
    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, 'app1/home.html', context)


@login_required
@csrf_exempt
def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post', post_slug=post_slug)
    else:
        form = CommentForm()

    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'app1/post.html', context)


@login_required
def comment_delete(request, post_slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        messages.error(request, 'Произошла ошибка!')
        return redirect('post', post_slug=post_slug)
    else:
        comment.delete()
        return redirect('post', post_slug=post_slug)


@login_required
@csrf_exempt
def edit_comment(request, post_slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        messages.error(request, 'Произошла ошибка!')
        return redirect('post', post_slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('post', post_slug=post_slug)
    else:
        form = CommentForm(instance=comment)

    context = {'form': form, 'comment': comment}
    return render(request, 'app1/edit_comment.html', context)


@login_required
def my_profile(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'app1/my_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_profile(request, username):
    user_to_view = get_object_or_404(User, username=username)
    user_form = UserEditForm(instance=user_to_view)
    profile_form = ProfileEditForm(instance=user_to_view.profile)
    posts = Post.objects.filter(author=user_to_view)
    context = {'user_form': user_form, 'profile_form': profile_form, 'posts': posts}
    return render(request, 'app1/view_profile.html', context)


@login_required
def like(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    return redirect('post', post_slug=post_slug)