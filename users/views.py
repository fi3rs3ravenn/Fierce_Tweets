from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, EditProfileForm
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/profile.html', {'user': user})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def follow_user_view(request, username):
    user_to_follow = get_object_or_404(CustomUser, username=username)
    if request.user != user_to_follow:
        if user_to_follow in request.user.following.all():
            request.user.following.remove(user_to_follow)
        else:
            request.user.following.add(user_to_follow)
    return redirect('profile', username=username)