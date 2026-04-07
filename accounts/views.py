from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile


#  Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            role = form.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Registration failed ❌")

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


#  Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, 'accounts/login.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('login')