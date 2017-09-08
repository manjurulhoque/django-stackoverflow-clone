# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-08 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0013_auto_20170909_0124'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.CharField(max_length=20)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
            ],
        ),
        migrations.RemoveField(
            model_name='vote',
            name='total',
        ),
    ]
