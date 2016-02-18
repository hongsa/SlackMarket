# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0006_auto_20160207_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='is_check',
            field=models.BooleanField(default=False),
        ),
    ]
