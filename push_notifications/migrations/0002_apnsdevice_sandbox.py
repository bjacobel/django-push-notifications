# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apnsdevice',
            name='sandbox',
            field=models.BooleanField(default=True, verbose_name='Use gateway.sandbox.push.apple.com?'),
            preserve_default=True,
        ),
    ]
