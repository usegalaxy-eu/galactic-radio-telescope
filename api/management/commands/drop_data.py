from api.models import Job, JobParam, MetricNumeric, MetricText

from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        print(Job.objects.all().delete())
        print(JobParam.objects.all().delete())
        print(MetricNumeric.objects.all().delete())
        print(MetricText.objects.all().delete())
