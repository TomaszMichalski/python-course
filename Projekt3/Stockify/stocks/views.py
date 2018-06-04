from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from stocks.forms import RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from . import models
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, 'stocks/index.html', {})

def main(request):
    if not request.user.is_authenticated:
        return redirect('index')
    profile = models.Profile.objects.get(user=request.user)
    wallet = str(profile.wallet)
    return render(request, 'stocks/main.html', { 'dollars': wallet[:-2], 'cents': wallet[-2:] })

def browse(request):
    if not request.user.is_authenticated:
        return redirect('index')
    stocks = models.Stock.objects.all()
    return render(request, 'stocks/browse.html', { 'stocks': stocks })

def manage(request):
    if not request.user.is_authenticated:
        return redirect('index')
    profile = models.Profile.objects.get(user=request.user)
    stocks = models.ProfileStock.objects.filter(profile=profile)
    return render(request, 'stocks/manage.html', { 'stocks': stocks })

def history(request):
    if not request.user.is_authenticated:
        return redirect('index')
    profile = models.Profile.objects.get(user=request.user)
    transactions = models.Transaction.objects.filter(profile=profile)
    return render(request, 'stocks/history.html', { 'transactions': transactions })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            profile = models.Profile(user=user)
            profile.save()
            for stock in models.Stock.objects.all():
                profile_stock = models.ProfileStock(profile=profile, stock=stock)
                profile_stock.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', { 'form': form })

def page_not_found(request):
    return render(request, 'other/error.html', {})
