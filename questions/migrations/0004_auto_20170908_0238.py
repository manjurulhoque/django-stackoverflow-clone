# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-07 20:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='vote',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='questions.Vote'),
            preserve_default=False,
        ),
    ]