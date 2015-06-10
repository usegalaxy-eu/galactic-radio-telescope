# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalaxyInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('dnsdomainname', models.CharField(max_length=64)),
                ('ipv4addr', models.CharField(max_length=16)),
                ('humanname', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('users_recent', models.IntegerField(default=0)),
                ('users_active', models.IntegerField(default=0)),
                ('users_total', models.IntegerField(default=0)),
                ('jobs_run', models.IntegerField(default=0)),
            ],
        ),
    ]
