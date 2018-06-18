"""
GRT Models
"""
from __future__ import unicode_literals

import os
import uuid as pyuuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class GalaxyInstance(models.Model):
    """A single galaxy site. Corresponds to a single galaxy.ini"""
    # Optional
    url = models.URLField(null=True, help_text="Instance URL")
    title = models.CharField(max_length=256, null=True, help_text="The name / title of the instance. E.g. GalaxyP")
    description = models.TextField(null=True, help_text="Any extra description you wish to add.")
    # The instance's information should be published. This will include a
    # logo/domain name page for each instance.

    users_recent = models.IntegerField(default=0)
    users_total = models.IntegerField(default=0)
    jobs_run = models.IntegerField(default=0)
    jobs_total = models.IntegerField(default=0)

    # Owner of this Galaxy instance
    owners = models.ManyToManyField(User)

    # API key for submitting results regarding this Galaxy instance
    api_key = models.UUIDField(default=pyuuid.uuid4, editable=False)

    # We import data on a cron job, we use this to track which was the most
    # recent data file that we imported.
    last_import = models.FloatField(default=-1)

    @property
    def report_dir(self):
        instance_report_dir = os.path.join(settings.GRT_UPLOAD_DIRECTORY, str(self.id))
        if not os.path.exists(instance_report_dir):
            os.makedirs(instance_report_dir)
        return instance_report_dir

    def uploaded_reports(self):
        """Get the set of reports that have previously been uploaded to GRT"""
        return [path.strip('.json') for path in os.listdir(self.report_dir) if path.endswith('.json')]

    def new_reports(self):
        """Get reports that have not yet been imported."""
        return [path for path in self.uploaded_reports() if float(path) > self.last_import]

    def get_absolute_url(self):
        return reverse('galaxy-instance-detail', kwargs={'slug': self.pk})

    def __str__(self):
        return '%s <%s>' % (self.title, self.url)


class Job(models.Model):
    """
    A single galaxy job
    """
    id = models.BigAutoField(primary_key=True)
    # Galaxy Instance
    instance = models.ForeignKey(GalaxyInstance)

    # We store the job ID from their database in order to ensure that we do not
    # create duplicate records.
    external_job_id = models.BigIntegerField()
    # Other attributes
    tool_id = models.CharField(max_length=255, null=True)
    tool_version = models.TextField(null=True)
    state = models.CharField(max_length=16, null=True)
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
    id = models.BigAutoField(primary_key=True)
    instance = models.ForeignKey(GalaxyInstance)
    external_job_id = models.BigIntegerField()
    name = models.CharField(max_length=256, null=True)
    value = models.TextField(null=True)


class MetricNumeric(models.Model):
    """
    Tuple of (name, type, value).
    """
    id = models.BigAutoField(primary_key=True)
    instance = models.ForeignKey(GalaxyInstance)
    external_job_id = models.BigIntegerField()
    plugin = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=256, null=True)
    value = models.DecimalField(max_digits=26, decimal_places=7)


class MetricText(models.Model):
    """
    Tuple of (name, type, value).
    """
    id = models.BigAutoField(primary_key=True)
    instance = models.ForeignKey(GalaxyInstance)
    external_job_id = models.BigIntegerField()
    plugin = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=256, null=True)
    value = models.CharField(max_length=256, null=True)


class Dataset(models.Model):
    """
    Tuple of ('job_id', 'dataset_id', 'extension', 'file_size', 'param_name', 'type').
    """
    id = models.BigAutoField(primary_key=True)
    instance = models.ForeignKey(GalaxyInstance)

    external_job_id = models.BigIntegerField()
    external_dataset_id = models.BigIntegerField()
    extension = models.CharField(max_length=32, null=True)
    file_size = models.BigIntegerField(null=True)
    param_name = models.CharField(max_length=256, null=True)
    file_type = models.CharField(max_length=16)

    def copy_file_size_template(self):
        return """
            CASE
                WHEN "%(name)s" = 'None' THEN NULL
                ELSE "%(name)s"::bigint
        """
