# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-04-06 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=32, unique=True, verbose_name='手机号')),
                ('nickname', models.CharField(max_length=128, unique=True, verbose_name='昵称')),
                ('sex', models.CharField(choices=[('female', 'female'), ('male', 'male')], max_length=8, verbose_name='性别')),
                ('birth_year', models.IntegerField(default=2000, verbose_name='出生年')),
                ('birth_month', models.IntegerField(default=1, verbose_name='出生月')),
                ('birth_day', models.IntegerField(default=1, verbose_name='出生日')),
                ('avatar', models.CharField(max_length=256, verbose_name='个人形象')),
                ('location', models.CharField(max_length=128, verbose_name='常居地')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
