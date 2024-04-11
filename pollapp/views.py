from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,  'You have successfully logged in.')
            return render(request, 'polls/home.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'polls/login.html')
    else:
        return render(request, 'polls/login.html')



def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('polls:home')


def home(request):
    return render(request, 'polls/login.html')


def signup(request):
    