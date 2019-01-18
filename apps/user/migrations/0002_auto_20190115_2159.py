# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserInfo',
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(verbose_name='地址的主人', to=settings.AUTH_USER_MODEL, to_field='id'),
        ),
    ]
