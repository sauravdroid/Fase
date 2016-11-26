# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-26 05:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('User', '0002_citrusresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=510, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('adress', models.TextField()),
                ('city', models.CharField(default=b'none', max_length=255)),
                ('state', models.CharField(default=b'none', max_length=255)),
                ('phone_no', models.CharField(default=b'none', max_length=255, unique=True)),
                ('pincode', models.IntegerField()),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='favoriteshop',
            name='fseller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.Seller'),
        ),
        migrations.AddField(
            model_name='favoriteshop',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
