# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0003_auto_20160204_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook')], max_length=10, default='facebook')),
                ('oauth_user_id', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='login_with_oauth',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facebookuser',
            name='user',
            field=models.ForeignKey(related_name='facebook_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
