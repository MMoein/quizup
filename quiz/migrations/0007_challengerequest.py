# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0006_auto_20160419_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(verbose_name=b'Category', to='quiz.QuestionCategory')),
                ('user', models.ForeignKey(verbose_name=b'Category', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
