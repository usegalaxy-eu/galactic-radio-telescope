import json
import tarfile
import os

from web.models import GalaxyInstance

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

        # Now load the report data.
        # with tarfile.open(report_base + '.tar.gz', 'r:gz') as handle:
            # files = {self.fix_name(member.name): member for member in mhandle}
            # # Process jobs first.
            # with transaction.atomic():
                # for job in f:
                    # (job_id, tool_id, state) = job.decode('utf-8').rstrip('\n').split('\t')
                    # Job.objects.create(
                        # instance=instance,
                        # tool=Tool.objects.get_or_create(tool_id)
                    # )
                    # # print(job_id, tool_id, state)
