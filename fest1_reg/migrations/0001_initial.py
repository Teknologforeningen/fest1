# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('quota', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('avec', models.CharField(max_length=128)),
                ('alcohol', models.BooleanField()),
                ('comment', models.TextField()),
                ('organization', models.ForeignKey(db_column='participants', to='fest1_reg.Organizations')),
            ],
        ),
    ]
