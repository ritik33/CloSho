from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, UpdateProfileForm, UpdatePasswordForm
from .models import User
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created')
            return redirect('login')
    else:
        form = SignupForm
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are successfully logged in.')
                return redirect('shop')
    else:
        if request.user.is_authenticated:
            return redirect('shop')
        form = LoginForm
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.warning(request, 'You have successfully logged out.')
    return redirect('shop')


@login_required
def profile(request):
    username = request.user
    user_info = User.objects.get(username=username)
    context = {'user_info': user_info}
    return render(request, 'profile.html', context)


@login_required
def updateProfile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated.')
            return redirect('profile')
        else:
            messages.warning(request, 'Invalid form data.')
            return redirect('update-profile')
    else:
        form = UpdateProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'update-profile.html', context)


@login_required
def updatePassword(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            auth.update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        else:
            messages.warning(request, 'Invalid password.')
            return redirect('update-password')
    else:
        form = UpdatePasswordForm(user=request.user)
        context = {'form': form}
        return render(request, 'update-password.html', context)
