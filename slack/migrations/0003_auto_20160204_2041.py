# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0002_auto_20160204_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
