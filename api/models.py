from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
import tagulous
import uuid as pyuuid

class Tool(models.Model):
    """A single tool"""
    id = models.UUIDField(primary_key=True, default=pyuuid.uuid4, editable=False)

    tool_id = models.CharField(max_length=128)
    tool_name = models.CharField(max_length=64)

    def __str__(self):
        return '%s [%s]' % (self.tool_id, self.tool_name)

    @property
    def found_in(self):
        return set([
            job.instance
            for job in self.job_set.all()
            if job.instance.public
        ])

    @property
    def instance_count(self):
        return len(self.found_in)


class ToolVersion(models.Model):
    """A version of a single tool"""
    tool = models.ForeignKey(Tool)
    version = models.CharField(max_length=32)

    def __str__(self):
        return '%s==%s' % (self.tool.tool_id, self.version)


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
    users_recent = models.ManyToManyField(IntegerDataPoint, related_name='user_recent_data', blank=True)
    users_total = models.ManyToManyField(IntegerDataPoint, related_name='user_total_data', blank=True)
    # Aggregate Job Data
    jobs_run = models.ManyToManyField(IntegerDataPoint, related_name='job_recent_data', blank=True)

    norm_users_recent = models.IntegerField(default=0)

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    # Tools installed on the server. This will allow searching through all
    # Galaxies for a particular tool.
    # tool_counts = models.ManyToManyField(IntegerDataPoint, related_name='tools_recent_data', blank=True)
    tools = models.ManyToManyField(Tool, blank=True)

    tags = tagulous.models.TagField()

    # Owner of this Galaxy instance
    owner = models.ForeignKey(User)
    # API key for submitting results regarding this Galaxy instance. Must
    # remain secure!!
    api_key = models.UUIDField(default=pyuuid.uuid4, editable=False)

    def __str__(self):
        return '%s <%s>' % (self.humanname, self.url)

    def get_absolute_url(self):
        return reverse_lazy('galaxy-instance-detail', kwargs={'slug': self.uuid})

    @property
    def latest_users_total(self):
        if self.users_total.count() > 0:
            return [x.value for x in self.users_total.all().order_by('-date')[0:1]][0]
        else:
            return 0

    @property
    def users_recent_data(self):
        if self.users_recent.count() > 0:
            return [x.value for x in self.users_recent.all().order_by('-date')[0:1]][0]
        else:
            return 0

    @property
    def users_total_data(self):
        if self.users_total.count() > 0:
            return [x.value for x in self.users_total.all().order_by('-date')[0:1]][0]
        else:
            return 0

    @property
    def jobs_run_data(self):
        if self.jobs_run.count() > 0:
            return [x.value for x in self.jobs_run.all().order_by('-date')[0:1]][0]
        else:
            return 0

    @property
    def tool_set(self):
        tools = set([job.tool for job in self.job_set.all()])
        return tools

    @property
    def tool_set_size(self):
        return len(self.tool_set)

    def spark_users(self):
        return ','.join([str(x.value) for x in self.users_recent.all().order_by('-date')[0:10]])

    def spark_jobs(self):
        return ','.join([str(x.value) for x in self.jobs_run.all().order_by('-date')[0:10]])


class Job(models.Model):
    ## Galaxy Instance
    instance = models.ForeignKey(GalaxyInstance)

    ## Tool
    tool = models.ForeignKey(Tool)
    # These are normalized to help with queries.
    tool_name = models.CharField(max_length=64)
    tool_version = models.CharField(max_length=64)

    ## Run Information
    date = models.DateTimeField(null=True, blank=True)
    # Tool params
    params = JSONField()

    # Metrics/collectl
    metrics_core_runtime_seconds = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    metrics_meminfo_swaptotal = models.IntegerField(blank=True, null=True)
    metrics_meminfo_memtotal = models.IntegerField(blank=True, null=True)
    metrics_core_galaxy_slots = models.IntegerField(default=0)
