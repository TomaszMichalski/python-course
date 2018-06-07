from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=10)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.CharField(max_length=32, default="100000.00")

class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    amount = models.CharField(max_length=32)
    value = models.CharField(max_length=32)
    cost = models.CharField(max_length=32)
    balance = models.CharField(max_length=32)
    sell = models.BooleanField()

class ProfileStock(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stocks = models.IntegerField(default=0)
