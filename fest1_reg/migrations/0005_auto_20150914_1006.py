# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fest1_reg', '0004_auto_20150914_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='organization',
            field=models.ForeignKey(db_column='participants', to='fest1_reg.Organization'),
        ),
    ]
