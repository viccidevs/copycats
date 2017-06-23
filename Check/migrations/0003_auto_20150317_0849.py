# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Check', '0002_auto_20150311_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuple',
            name='id',
        ),
        migrations.AlterField(
            model_name='tuple',
            name='filesId',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
