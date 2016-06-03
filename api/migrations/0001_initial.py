# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-03 17:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalaxyInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', uuidfield.fields.UUIDField(blank=True, editable=False, max_length=32, unique=True)),
                ('dnsdomainname', models.CharField(blank=True, max_length=64, null=True)),
                ('humanname', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('users_recent', models.CommaSeparatedIntegerField(max_length=32)),
                ('users_total', models.CommaSeparatedIntegerField(max_length=32)),
                ('jobs_run', models.CommaSeparatedIntegerField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_id', models.CharField(max_length=128)),
                ('tool_version', models.CharField(max_length=32)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(max_length=30)),
                ('params', jsonfield.fields.JSONField()),
                ('metrics_core_runtime_seconds', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('metrics_meminfo_swaptotal', models.IntegerField(blank=True, null=True)),
                ('metrics_meminfo_memtotal', models.IntegerField(blank=True, null=True)),
                ('metrics_cpuinfo_processor_count', models.IntegerField(default=0)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.GalaxyInstance')),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_id', models.CharField(max_length=128)),
                ('tool_version', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='galaxyinstance',
            name='tools',
            field=models.ManyToManyField(to='api.Tool'),
        ),
    ]