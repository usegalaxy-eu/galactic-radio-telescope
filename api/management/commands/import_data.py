import json
import tarfile
import os

from api.models import GalaxyInstance

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Load all data from the report directory.'

    def handle(self, *args, **options):
        report_dir = settings.GRT_UPLOAD_DIRECTORY
        for instance in GalaxyInstance.objects.all():
            for report_id in instance.new_reports():
                self.import_report(instance, report_id)

    def fix_name(self, name):
        if '.jobs.tsv' in member.name:
            return 'jobs'
        elif '.metric_num.tsv' in member.name:
            return 'metric_num'
        elif '.metric_txt.tsv' in member.name:
            return 'metric_txt'
        elif '.params.tsv' in member.name:
            return 'params'
        return 'unknown'

    def import_report(self, instance, report_id):
        report_base = os.path.join(instance.report_dir, report_id)

        # first load the metadata
        with open(report_base + '.json', 'r') as handle:
            meta = json.load(handle)

        instance.users_recent = meta['users']['active']
        instance.users_total = meta['users']['total']
        instance.jobs_run = meta['jobs']['ok']
        instance.last_import = report_id
        instance.save()
