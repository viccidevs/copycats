# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Check', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuple',
            name='file1',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tuple',
            name='file2',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
    ]
