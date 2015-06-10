""" Basic models, such as user profile """
from django.db import models
from uuidfield import UUIDField


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


#class Job(models.Model):
    #instance = models.ForeignKey(GalaxyInstance)

    ## Tool
    #tool_id = models.CharField(max_length=128)
    #tool_version = models.CharField(max_length=32)

    ## Run Information
    #start_date = models.DateField(null=True, blank=True)

