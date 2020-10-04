from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class users(models.Model):
    user_first_name=models.CharField(max_length=30)
    user_last_name=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    mobile=models.CharField(max_length=10)
    gmail=models.CharField(max_length=40,primary_key=True)

class share_owner(models.Model):
    user_gmail=models.CharField(max_length=40)
    date=models.DateField()
    company_code=models.CharField(max_length=20)
    company_name=models.CharField(max_length=100)
    share_quntity=models.IntegerField()
    share_price=models.IntegerField()
    total=models.IntegerField()

class sell_data_table(models.Model):
    user_gmail=models.CharField(max_length=40)
    company_code=models.CharField(max_length=20)
    company_name=models.CharField(max_length=100)
    buy_date=models.DateField()
    sell_date=models.DateField()
    buy_price=models.IntegerField()
    sell_price=models.IntegerField()
    total_sell_price=models.IntegerField()
    total_profit=models.IntegerField()
    sell_quntity=models.IntegerField()

    
