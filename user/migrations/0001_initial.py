# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-01-20 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('ugender', models.CharField(max_length=6)),
                ('ulogintime', models.DateTimeField()),
                ('ucontact', models.CharField(max_length=11)),
                ('uemail', models.CharField(max_length=20)),
                ('uposition', models.CharField(max_length=1)),
            ],
        ),
    ]
