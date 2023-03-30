from django.shortcuts import render
from .models import Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import PostForm


@csrf_exempt
def home(request):
    posts = Post.objects.order_by('-id')
    context = {'posts': posts}
    return render(request, 'home.html', context)


@login_required
@csrf_exempt
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('base')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'add_post.html', context)


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('name')
            else:
                print('User not found')
                pass
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration.html', context)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('name')
        else:
            print('User not found')
            pass

    return render(request, 'login.html')


def blog(request):
    return render(request, 'blog.html')


def contacts(request):
    return render(request, 'contacts.html')


@login_required
@csrf_exempt
def base(request):
    posts = Post.objects.order_by('-id')
    context = {'posts': posts}
    return render(request, 'base.html', context)


@login_required
def name(request):
    return render(request, 'name.html')


@login_required
@csrf_exempt
def user_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        if post.author == request.user:
            post.delete()
            return redirect('base')
    posts = Post.objects.filter(author=request.user)
    context = {'posts': posts}
    return render(request, 'user_post.html', context)