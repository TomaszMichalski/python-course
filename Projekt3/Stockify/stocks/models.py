from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=10)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.IntegerField(default=10000000) #100 000.00

class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    amount = models.IntegerField()
    value = models.IntegerField()
    cost = models.IntegerField()
    balance = models.IntegerField()
    sell = models.BooleanField()

class ProfileStock(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stocks = models.IntegerField(default=0)
