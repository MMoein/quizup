# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0002_auto_20160503_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='time_in_quiz',
            field=models.IntegerField(default=0),
        ),
    ]
