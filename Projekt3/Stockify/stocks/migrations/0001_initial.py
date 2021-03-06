# Generated by Django 2.0.5 on 2018-06-07 18:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def load_stock_markets(apps, schema_editor):
    Stock = apps.get_model("stocks", "Stock")
    stock_goldman = Stock(id=0, name='GS')
    stock_goldman.save()
    stock_apple = Stock(id=1, name='AAPL')
    stock_apple.save()
    stock_microsoft = Stock(id=2, name='MSFT')
    stock_microsoft.save()
    stock_ibm = Stock(id=3, name='IBM')
    stock_ibm.save()
    stock_jpmorgan = Stock(id=4, name='JPM')
    stock_jpmorgan.save()
    stock_intel = Stock(id=5, name='INTC')
    stock_intel.save()
    stock_cisco = Stock(id=6, name='CSCO')
    stock_cisco.save()
    stock_boeing = Stock(id=7, name='BA')
    stock_boeing.save()

def delete_stock_markets(apps, schema_editor):
    Stock = apps.get_model("stocks", "Stock")
    Stock.objects.all().delete()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.IntegerField(default=10000000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stocks', models.IntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('amount', models.IntegerField()),
                ('value', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('sell', models.BooleanField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Profile')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Stock')),
            ],
        ),
        migrations.AddField(
            model_name='profilestock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Stock'),
        ),
        migrations.RunPython(load_stock_markets),
    ]
