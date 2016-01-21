# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Slack',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(unique=True)),
                ('token', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
                ('type', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('nickname', models.CharField(unique=True, max_length=100)),
                ('password', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('sex', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='slack',
            name='user',
            field=models.ForeignKey(related_name='slack_user', to='slack.User'),
        ),
        migrations.AddField(
            model_name='register',
            name='slack',
            field=models.ForeignKey(related_name='register_slack', to='slack.Slack'),
        ),
        migrations.AddField(
            model_name='register',
            name='user',
            field=models.ForeignKey(related_name='register_user', to='slack.User'),
        ),
    ]
