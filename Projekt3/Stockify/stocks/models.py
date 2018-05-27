from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=10)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.IntegerField()
    value = models.IntegerField()
    cost = models.IntegerField()
    balance = models.IntegerField()

class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stocks = models.IntegerField()
