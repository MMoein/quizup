# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='competitor2',
            field=models.ForeignKey(related_name='second_competitor', blank=True, to='Authentication.UserProfile', null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=quiz.models.ListField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='score1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='score2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='start_time2',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
