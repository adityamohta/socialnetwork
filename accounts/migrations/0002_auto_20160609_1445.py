# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 09:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
