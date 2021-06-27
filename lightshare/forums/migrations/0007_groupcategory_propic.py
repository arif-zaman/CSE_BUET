# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0006_auto_20141025_0431'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcategory',
            name='propic',
            field=models.FileField(null=True, upload_to=b'Files/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
