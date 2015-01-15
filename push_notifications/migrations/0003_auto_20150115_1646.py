# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0002_apnsdevice_sandbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apnsdevice',
            name='registration_id',
            field=models.CharField(max_length=64, verbose_name='Registration ID'),
            preserve_default=True,
        ),
    ]
