# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20160405_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='answered_count1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='answered_count2',
            field=models.IntegerField(default=0),
        ),
    ]
