# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(unique=True, max_length=200)),
                ('group_creator', models.CharField(max_length=120)),
                ('group_category', models.CharField(max_length=120, db_index=True)),
                ('public', models.BooleanField(default=True)),
                ('group_description', models.CharField(max_length=1500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['group_category'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('writer', models.CharField(max_length=120)),
                ('body', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('group_name', models.CharField(max_length=200, db_index=True)),
                ('pfile', models.ImageField(null=True, upload_to=b'Image/%Y/%m/%d', blank=True)),
                ('likes', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_category', models.CharField(unique=True, max_length=120)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['group_category'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=120)),
                ('group_name', models.CharField(max_length=200, db_index=True)),
                ('status', models.CharField(max_length=120)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['username'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post_Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=1200)),
                ('commentor', models.CharField(max_length=120)),
                ('post_id', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['post_id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post_Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=120)),
                ('post_id', models.IntegerField(db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['post_id'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='post_like',
            unique_together=set([('username', 'post_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupmember',
            unique_together=set([('username', 'group_name')]),
        ),
    ]
