"""
GRT Models
"""
from __future__ import unicode_literals

import os
import uuid as pyuuid

import tagulous

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User


class GalaxyInstance(models.Model):
    """A single galaxy site. Corresponds to a single galaxy.ini"""
    id = models.UUIDField(primary_key=True, default=pyuuid.uuid4, editable=False)
    # Optional
    url = models.URLField(null=True, help_text="Publicly accesible instance URL")
    title = models.CharField(max_length=256, null=True, help_text="The name / title of the instance. E.g. GalaxyP")
    description = models.TextField(null=True, help_text="Any extra description you wish to add.")
    # The instance's information should be published. This will include a
    # logo/domain name page for each instance.
    public = models.BooleanField(default=False, help_text="Is the instance open to the public?")

    users_recent = models.TextField(blank=True)
    users_total = models.TextField(blank=True)
    jobs_run = models.TextField(blank=True)

    # Owner of this Galaxy instance
    owners = models.ManyToManyField(User)

    # API key for submitting results regarding this Galaxy instance
    api_key = models.UUIDField(default=pyuuid.uuid4, editable=False)

    # We import data on a cron job, we use this to track which was the most
    # recent data file that we imported.
    last_import = models.FloatField(default=-1)

    @property
    def report_dir(self):
        uuid = str(self.id)
        instance_report_dir = os.path.join(settings.GRT_UPLOAD_DIRECTORY, uuid[0:2], uuid[2:4], uuid)
        if not os.path.exists(instance_report_dir):
            os.makedirs(instance_report_dir)
        return instance_report_dir

    def uploaded_reports(self):
        """Get the set of reports that have previously been uploaded to GRT"""
        return [path.strip('.json') for path in os.listdir(self.report_dir) if path.endswith('.json')]

    def new_reports(self):
        """Get reports that have not yet been imported."""
        return [path for path in self.uploaded_reports() if float(path) > self.last_import]

    def __str__(self):
        return '%s <%s>' % (self.title, self.url)


class Job(models.Model):
    """
    A single galaxy job
    """
    # Galaxy Instance
    instance = models.ForeignKey(GalaxyInstance)

    # We store the job ID from their database in order to ensure that we do not
    # create duplicate records.
    external_job_id = models.IntegerField(default=-1)
    # Other attributes
    tool_id= models.CharField(max_length=255)
    tool_version = models.TextField()
    state = models.CharField(max_length=16)
    create_time = models.DateTimeField(null=True, blank=True)

    # Ensure that the combination of instance + external_job_id is unique. We
    # don't want duplicate jobs skewing our results.
    class Meta:
        unique_together = (('instance', 'external_job_id'),)


class JobParam(models.Model):
    """
    A given parameter within a job. For non-repeats, these are simple
    (some_param, 10), for repeats and other more complex ones, this comes as a
    giant JSON struct.
    """
    job = models.ForeignKey(Job)
    name = models.CharField(max_length=256)
    value = models.TextField()


class MetricNumeric(models.Model):
    """
    Tuple of (name, type, value).
    """
    job = models.ForeignKey(Job)
    plugin = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    value = models.DecimalField()


class MetricText(models.Model):
    """
    Tuple of (name, type, value).
    """
    job = models.ForeignKey(Job)
    plugin = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
