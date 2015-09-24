# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fest1_reg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('avec', models.CharField(max_length=128)),
                ('alcohol', models.BooleanField()),
                ('comment', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Organizations',
            new_name='Organization',
        ),
        migrations.RemoveField(
            model_name='participants',
            name='organization',
        ),
        migrations.DeleteModel(
            name='Participants',
        ),
        migrations.AddField(
            model_name='participant',
            name='organization',
            field=models.ForeignKey(db_column='participants', to='fest1_reg.Organization'),
        ),
    ]
