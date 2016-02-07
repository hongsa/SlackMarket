# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0005_auto_20160207_1749'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facebookuser',
            old_name='updated_at',
            new_name='updated_time',
        ),
    ]
