# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151129_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='project',
            field=models.ForeignKey(to='app.Project', default=1),
            preserve_default=False,
        ),
    ]
