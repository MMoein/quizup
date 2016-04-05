# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
        ('quiz', '0002_auto_20160309_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time1', models.DateTimeField()),
                ('score1', models.IntegerField()),
                ('start_time2', models.DateTimeField()),
                ('score2', models.IntegerField()),
                ('questions', quiz.models.ListField()),
                ('category', models.ForeignKey(verbose_name=b'Category', to='quiz.QuestionCategory')),
                ('competitor1', models.ForeignKey(related_name='first_competitor', to='Authentication.UserProfile')),
                ('competitor2', models.ForeignKey(related_name='second_competitor', to='Authentication.UserProfile')),
            ],
        ),
    ]
