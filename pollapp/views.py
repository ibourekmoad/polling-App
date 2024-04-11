from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'login.html',{'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')


    return None


def logout(request):
    logout(request)
    return render(request, 'login.html')
