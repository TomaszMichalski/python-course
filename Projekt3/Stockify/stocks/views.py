from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from stocks.forms import RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from . import models
from . import helpers
import pandas
#hax for current versions of pandas and pandas_datareader (06.05.2018)
pandas.core.common.is_list_like = pandas.api.types.is_list_like
import pandas_datareader.data as web
import quandl
from datetime import datetime, timedelta
# Create your views here.

quandl.ApiConfig.api_key = "Jc6Qyrb7yVunuhwUbKyL"

def index(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, 'stocks/index.html', {})

def main(request):
    if not request.user.is_authenticated:
        return redirect('index')
    profile = models.Profile.objects.get(user=request.user)
    return render(request, 'stocks/main.html', { 'wallet': profile.wallet_string })

def browse(request):
    if not request.user.is_authenticated:
        return redirect('index')
    stocks = models.Stock.objects.all()
    errors = []
    profile = models.Profile.objects.get(user=request.user)
    if request.method == "POST":
        stock_name = request.POST['stock_name']
        amount = request.POST['amount']
        price = helpers.money_as_int(request.POST['price'])
        if not helpers.is_integer(amount):
            errors.append("Stock amount should be an integer")
        else:
            amount = int(amount)
        if not errors and amount * price > profile.wallet:
            errors.append("Insufficient funds")
        if not errors:
            stock = models.Stock.objects.get(name=stock_name)
            profile_stock = models.ProfileStock.objects.get(profile=profile, stock=stock)
            profile_stock.stocks += amount
            profile_stock.save()
            transaction = models.Transaction(profile=profile, stock=stock, date=datetime.today(), amount=amount, value=price, cost=amount * price, balance=profile.wallet - amount * price, sell=False)
            transaction.save()
            profile.wallet -= amount * price
            profile.save()
    return render(request, 'stocks/browse.html', { 'stocks': stocks, 'price': helpers.money_as_string(20), 'change': 1.23, 'errors': errors, 'wallet': profile.wallet_string })


def chart(request, name):
    if not request.user.is_authenticated:
        return redirect('index')
    stock = models.Stock.objects.get(name=name)
    if stock is None:
        return redirect('browse')
    end = datetime.today()
    start = end - timedelta(days=30)
    data = quandl.get("WIKI/AAPL", rows=5)
    return render(request, 'stocks/chart.html', { 'stock': stock, 'data': data.Close })

def manage(request):
    if not request.user.is_authenticated:
        return redirect('index')
    profile = models.Profile.objects.get(user=request.user)
    stocks = models.ProfileStock.objects.filter(profile=profile)
    errors = []
    if request.method == "POST":
        stock_name = request.POST['stock_name']
        price = helpers.money_as_int(request.POST['price'])
        stock = models.Stock.objects.get(name=stock_name)
        profile_stock = models.ProfileStock.objects.get(stock=stock)
        amount = request.POST['amount']
        if not helpers.is_integer(amount):
            errors.append("Stock amount should be an integer")
        else:
            amount = int(amount)
        if not errors and amount > profile_stock.stocks:
            errors.append("Not enough stocks")
        profile = models.Profile.objects.get(user=request.user)
        if not errors:
            profile_stock.stocks -= amount
            profile_stock.save()
            transaction = models.Transaction(profile=profile, stock=stock, date=datetime.today(), amount=amount, value=price, cost=amount * price, balance=profile.wallet - amount * price, sell=True)
            transaction.save()
            profile.wallet += amount * price
            profile.save()
    return render(request, 'stocks/manage.html', { 'stocks': stocks, 'price': helpers.money_as_string(20), 'errors': errors, 'wallet': profile.wallet_string })

def history(request):
    if not request.user.is_authenticated:
        return redirect('index')
    profile = models.Profile.objects.get(user=request.user)
    transactions = models.Transaction.objects.filter(profile=profile).order_by('-date')
    return render(request, 'stocks/history.html', { 'transactions': transactions, 'wallet': profile.wallet_string })

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
