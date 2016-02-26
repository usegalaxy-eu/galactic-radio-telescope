from __future__ import unicode_literals
from django.db import models
from uuidfield import UUIDField
from jsonfield import JSONField


class GalaxyInstance(models.Model):
    uuid = UUIDField(auto=True)
    # Need not be provided
    dnsdomainname = models.CharField(max_length=64, null=True, blank=True)
    humanname = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    # The instance's information should be published. This will include a
    # logo/domain name page for each instance (eventually). This will allow GRT
    # to function as a galaxy directory for sorts.
    #
    # An admin will have to register their instance with GRT in order to make
    # it public
    public = models.BooleanField(default=False)

    # Aggregate User data
    users_recent = models.IntegerField(default=0)
    users_total = models.IntegerField(default=0)
    # Aggregate Job Data
    jobs_run = models.IntegerField(default=0)

class Job(models.Model):
    ## Galaxy Instance
    instance = models.ForeignKey(GalaxyInstance)

    ## Tool
    tool_id = models.CharField(max_length=128)
    tool_version = models.CharField(max_length=32)

    ## Run Information
    date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=30)
    # Tool params
    params = JSONField()

    # Metrics/collectl
    metrics_core_runtime_seconds = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    metrics_meminfo_swaptotal = models.IntegerField(blank=True, null=True)
    metrics_meminfo_memtotal = models.IntegerField(blank=True, null=True)
    metrics_cpuinfo_processor_count = models.IntegerField(default=0)
