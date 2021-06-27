# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0002_remove_grouparticle_pfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='isactive',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grouparticle',
            name='isactive',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
