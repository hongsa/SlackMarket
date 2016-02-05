# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=255, unique=True)),
                ('username', models.CharField(verbose_name='Username', max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.IntegerField(default=0)),
                ('description', models.TextField(default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slack',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200, unique=True)),
                ('token', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('type', models.IntegerField()),
                ('category', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='slack_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='register',
            name='slack',
            field=models.ForeignKey(related_name='register_slack', to='slack.Slack'),
        ),
        migrations.AddField(
            model_name='register',
            name='user',
            field=models.ForeignKey(related_name='register_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
