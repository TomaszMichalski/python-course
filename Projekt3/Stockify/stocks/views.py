from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from stocks.forms import RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, 'stocks/index.html', {})

def main(request):
    return render(request, 'stocks/main.html', {})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', { 'form': form })
