# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choice1',
            field=models.CharField(default='test', max_length=255, verbose_name=b'Right answer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='choice2',
            field=models.CharField(default='test', max_length=255, verbose_name=b'Dummy answer1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='choice3',
            field=models.CharField(default='test', max_length=255, verbose_name=b'Dummy answer2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='choice4',
            field=models.CharField(default='test', max_length=255, verbose_name=b'Dummy answer3'),
            preserve_default=False,
        ),
    ]
