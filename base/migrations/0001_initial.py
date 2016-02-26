# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
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
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tool_id', models.CharField(max_length=128)),
                ('tool_version', models.CharField(max_length=32)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('handler', models.CharField(max_length=60)),
                ('runner', models.CharField(max_length=60)),
                ('exit_code', models.IntegerField(null=True, blank=True)),
                ('state', models.CharField(max_length=30)),
                ('params', jsonfield.fields.JSONField()),
                ('metrics_core_start_epoch', models.DateTimeField(null=True, blank=True)),
                ('metrics_core_end_epoch', models.DateTimeField(null=True, blank=True)),
                ('metrics_core_galaxy_slots', models.IntegerField(default=0)),
                ('metrics_core_runtime_seconds', models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)),
                ('metrics_meminfo_swaptotal', models.IntegerField(null=True, blank=True)),
                ('metrics_meminfo_memtotal', models.IntegerField(null=True, blank=True)),
                ('metrics_cpuinfo_processor_count', models.IntegerField(default=0)),
                ('instance', models.ForeignKey(to='base.GalaxyInstance')),
            ],
        ),
    ]
