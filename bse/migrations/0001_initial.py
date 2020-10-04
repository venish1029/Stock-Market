# Generated by Django 3.0.5 on 2020-10-04 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sell_data_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_gmail', models.CharField(max_length=40)),
                ('company_code', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=100)),
                ('buy_date', models.DateField()),
                ('sell_date', models.DateField()),
                ('buy_price', models.IntegerField()),
                ('sell_price', models.IntegerField()),
                ('total_sell_price', models.IntegerField()),
                ('total_profit', models.IntegerField()),
                ('sell_quntity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='share_owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_gmail', models.CharField(max_length=40)),
                ('date', models.DateField()),
                ('company_code', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=100)),
                ('share_quntity', models.IntegerField()),
                ('share_price', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_first_name', models.CharField(max_length=30)),
                ('user_last_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=10)),
                ('gmail', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
        ),
    ]
