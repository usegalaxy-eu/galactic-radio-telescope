""" Basic models, such as user profile """
from django.db import models
from uuidfield import UUIDField
from jsonfield import JSONField
import datetime

class GalaxyInstance(models.Model):
    uuid = UUIDField(auto=True)

    # Store domain name for public viewing, if public==true
    dnsdomainname = models.CharField(max_length=64)
    # This is used to uniquely distinguish galaxy instances. It MUST be public.
    # TODO: Find a better way to distinguish galaxy instances. Maybe hash of
    # SECRET_KEY + external_ip ?
    ipv4addr = models.CharField(max_length=16)
    # TODO: Should we use the contents of the branding variable? Or a custom
    # string?
    humanname = models.CharField(max_length=256)
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
    users_active = models.IntegerField(default=0)
    users_total = models.IntegerField(default=0)

    # Aggregate Job Data
    jobs_run = models.IntegerField(default=0)

class ConvertUnixTimestamp(models.DateTimeField):
    def get_prep_value(self, value):
        return datetime.datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

class Job(models.Model):
    ## Galaxy Instance
    instance = models.ForeignKey(GalaxyInstance)

    ## Tool
    tool_id = models.CharField(max_length=128)
    tool_version = models.CharField(max_length=32)

    ## Run Information
    start_date = models.DateField(null=True, blank=True)
    handler = models.CharField(max_length=60)
    runner = models.CharField(max_length=60)
    exit_code = models.IntegerField(blank=True, null=True) # maybe PositiveSmallIntegerField?
    state = models.CharField(max_length=30)
    params = JSONField()
    metrics_core_start_epoch = ConvertUnixTimestamp(blank=True, null=True)
    metrics_core_end_epoch = ConvertUnixTimestamp(blank=True, null=True)
    metrics_core_galaxy_slots = models.IntegerField(default=0)
    metrics_core_runtime_seconds = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    metrics_meminfo_swaptotal = ConvertUnixTimestamp(blank=True, null=True)
    metrics_meminfo_memtotal = ConvertUnixTimestamp(blank=True, null=True)
    metrics_cpuinfo_processor_count = models.IntegerField(default=0)