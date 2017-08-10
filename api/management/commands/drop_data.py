from api.models import Job, JobParam, MetricNumeric, GalaxyInstance

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        print(Job.objects.all().delete())
        print(JobParam.objects.all().delete())
        print(MetricNumeric.objects.all().delete())
        for ins in GalaxyInstance.objects.all():
            ins.last_import = -1
            ins.save()
