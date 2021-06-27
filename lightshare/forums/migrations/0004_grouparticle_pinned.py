# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0003_auto_20141023_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouparticle',
            name='pinned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
