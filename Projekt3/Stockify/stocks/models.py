from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=10)

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    wallet = models.IntegerField()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.IntegerField()
    rate = models.IntegerField()
