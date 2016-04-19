# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20160419_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='score1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='score2',
            field=models.IntegerField(default=0),
        ),
    ]
