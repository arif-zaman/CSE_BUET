# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0004_grouparticle_pinned'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='propic',
            field=models.FileField(null=True, upload_to=b'Files/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
