# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0004_auto_20160206_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookuser',
            name='created_at',
        ),
        migrations.AddField(
            model_name='facebookuser',
            name='gender',
            field=models.CharField(default='male', max_length=10),
        ),
        migrations.AddField(
            model_name='facebookuser',
            name='locale',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
