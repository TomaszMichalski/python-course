from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from . import helpers
# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=10)

    @property
    def quandl_name(self):
        return "EOD/" + name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.IntegerField(default=10000000)

    @property
    def wallet_string(self):
        return helpers.money_as_string(self.wallet)

class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    amount = models.IntegerField()
    value = models.IntegerField()
    cost = models.IntegerField()
    balance = models.IntegerField()
    sell = models.BooleanField()

    @property
    def value_string(self):
        return helpers.money_as_string(self.value)

    @property
    def cost_string(self):
        if self.sell:
            return '+%s' % helpers.money_as_string(self.cost)
        else:
            return '-%s' % helpers.money_as_string(self.cost)

    @property
    def balance_string(self):
        return helpers.money_as_string(self.balance)

class ProfileStock(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stocks = models.IntegerField(default=0)
