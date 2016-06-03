from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
import uuid as pyuuid


class Tool(models.Model):
    """A single tool"""
    tool_id = models.CharField(max_length=128)
    tool_version = models.CharField(max_length=32)
    tool_name = models.CharField(max_length=64)

    def __str__(self):
        return '%s==%s' % (self.tool_id, self.tool_version)

class IntegerDataPoint(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=0)

class GalaxyInstance(models.Model):
    """A single galaxy site. Corresponds to a single galaxy.ini"""
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    uuid = models.UUIDField(default=pyuuid.uuid4, editable=False)
    # Need not be provided
    url = models.URLField(null=True, blank=True)
    humanname = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    # The instance's information should be published. This will include a
    # logo/domain name page for each instance (eventually). This will allow GRT
    # to function as a galaxy directory for sorts.
    public = models.BooleanField(default=False)

    # Aggregate User data. Only retain 32 data points for a nice graph.
    users_recent = models.ManyToManyField(IntegerDataPoint, related_name='user_recent_data')
    users_total = models.ManyToManyField(IntegerDataPoint, related_name='user_total_data')
    # Aggregate Job Data
    jobs_run = models.ManyToManyField(IntegerDataPoint, related_name='job_recent_data')

    # Tools installed on the server. This will allow searching through all
    # Galaxies for a particular tool.
    tools = models.ManyToManyField(Tool, blank=True)

    # Owner of this Galaxy instance
    owner = models.ForeignKey(User)
    # API key for submitting results regarding this Galaxy instance. Must
    # remain secure!!
    api_key = models.UUIDField(default=pyuuid.uuid4, editable=False)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse_lazy('galaxy-instance-detail', kwargs={'slug': self.uuid})

    @property
    def users_recent_data(self):
        return [x.value for x in self.users_recent.all().order_by('-date')[0:5]]

    @property
    def users_total_data(self):
        return [x.value for x in self.users_total.all().order_by('-date')[0:5]]

    @property
    def jobs_run_data(self):
        return [x.value for x in self.jobs_run.all().order_by('-date')[0:5]]

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
    metrics_cpuinfo_cores_allocated = models.IntegerField(default=0)
