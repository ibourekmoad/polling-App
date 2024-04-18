from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Poll, Choice
from .forms import PollForm, ChoiceForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'polls/login.html')
    else:
        return render(request, 'polls/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'polls/home.html')
    return render(request, 'polls/login.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'welcome ' + username)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'polls/registration.html', {'form': form})


@login_required
def create_poll(request):
    if request.method == 'POST':
        num_choices = sum(1 for key in request.POST.keys() if key.startswith('choice_'))
        poll_form = PollForm(request.POST)
        choice_forms = [ChoiceForm(request.POST, prefix=str(x)) for x in range(num_choices)]
        if poll_form.is_valid() and all([form.is_valid() for form in choice_forms]):
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            for form in choice_forms:
                choice = form.save(commit=False)
                choice.poll = poll
                choice.save()
            return redirect('home')
    else:
        poll_form = PollForm()
        choice_forms = [ChoiceForm(prefix=str(x)) for x in range(2)]
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'choice_forms': choice_forms})


@login_required
def list_polls(request):
    polls = Poll.objects.all()
    return render(request, 'polls/list_polls.html', {"polls": polls})


@login_required
def poll_detail(request, pk=None):
    poll = Poll.objects.get(pk=pk)
    choices = poll.choice_set.all()

    return render(request, 'polls/poll_detail.html', {'poll':poll, 'choices': choices})
