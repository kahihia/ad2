# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-19 10:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_profile', '0003_userwish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwish',
            name='product',
        ),
        migrations.DeleteModel(
            name='UserWish',
        ),
    ]