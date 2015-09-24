# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fest1_reg', '0005_auto_20150914_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='organization',
            field=models.ForeignKey(to='fest1_reg.Organization', db_column='participants_organization'),
        ),
    ]
