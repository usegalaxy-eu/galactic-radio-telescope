from __future__ import unicode_literals
from django.db import models
from uuidfield import UUIDField
from jsonfield import JSONField

class Tool(models.Model):
    """A single tool"""
    tool_id = models.CharField(max_length=128)
    tool_version = models.CharField(max_length=32)

    def __str__(self):
        return '%s==%s' % (self.tool_id, self.tool_version)

class GalaxyInstance(models.Model):
    """A single galaxy site. Corresponds to a single galaxy.ini"""
    uuid = UUIDField(auto=True)
    # Need not be provided
    url = models.URLField(null=True, blank=True)
    humanname = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    # The instance's information should be published. This will include a
    # logo/domain name page for each instance (eventually). This will allow GRT
    # to function as a galaxy directory for sorts.
    public = models.BooleanField(default=False)

    # Aggregate User data. Only retain 32 data points for a nice graph.
    users_recent = models.CommaSeparatedIntegerField(max_length=32)
    users_total = models.CommaSeparatedIntegerField(max_length=32)
    # Aggregate Job Data
    jobs_run = models.CommaSeparatedIntegerField(max_length=32)

    # Tools installed on the server. This will allow searching through all
    # Galaxies for a particular tool.
    tools = models.ManyToManyField(Tool, blank=True, null=True)

    def __str__(self):
        return self.url

class Job(models.Model):
    ## Galaxy Instance
    instance = models.ForeignKey(GalaxyInstance)

    ## Tool
    tool = models.ForeignKey(Tool)

    ## Run Information
    date = models.DateTimeField(null=True, blank=True)
    # Tool params
    params = JSONField()

    # Metrics/collectl
    metrics_core_runtime_seconds = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    metrics_meminfo_swaptotal = models.IntegerField(blank=True, null=True)
    metrics_meminfo_memtotal = models.IntegerField(blank=True, null=True)
    metrics_cpuinfo_processor_count = models.IntegerField(default=0)
