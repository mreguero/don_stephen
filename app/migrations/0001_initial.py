# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('finality', models.CharField(max_length=255)),
                ('who', models.CharField(max_length=255)),
                ('purpose', models.CharField(max_length=255)),
                ('ffile', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('given', models.CharField(max_length=255)),
                ('when', models.CharField(max_length=255)),
                ('then', models.CharField(max_length=255)),
                ('feature', models.ForeignKey(to='app.Feature', related_name='scenario')),
            ],
        ),
    ]
