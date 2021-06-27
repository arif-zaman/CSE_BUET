# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0005_group_propic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouparticle',
            options={'ordering': ['-pinned', '-created']},
        ),
        migrations.AddField(
            model_name='groupmember',
            name='is_verified',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
