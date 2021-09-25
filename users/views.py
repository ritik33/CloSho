from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
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
                return redirect('home')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.warning(request, 'You have successfully logged out.')
    return redirect('home')


@login_required
def profile(request):  # , username):
    # data = User.objects.all(username=username)
    # context = {'data': data}
    return render(request, 'profile.html')  # , context)
