# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tuple',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file1', models.FileField(upload_to=b'/checkercodes/')),
                ('file2', models.FileField(upload_to=b'/checkercodes/')),
                ('filesId', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
