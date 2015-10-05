# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150929_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demouser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=15, unique=True, null=True, blank=True),
        ),
    ]
