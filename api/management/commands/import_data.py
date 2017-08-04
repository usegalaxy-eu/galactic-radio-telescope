# import json
# import tarfile
# import os

from api.models import GalaxyInstance, Job, JobParam, MetricNumeric, MetricText

from django.core.management.base import BaseCommand
# from django.conf import settings
# from django.db import transaction
# from django.contrib.auth.models import User
from postgres_copy import CopyMapping


class Command(BaseCommand):
    help = 'Load all data from the report directory.'

    def handle(self, *args, **options):
        # report_dir = settings.GRT_UPLOAD_DIRECTORY
        for instance in GalaxyInstance.objects.all():
            for report_id in instance.new_reports():
                self.import_report(instance, report_id)

    def fix_name(self, member):
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
        # report_base = os.path.join(instance.report_dir, report_id)

        # first load the metadata
        # with open(report_base + '.json', 'r') as handle:
            # meta = json.load(handle)

        c = CopyMapping(
            Job,
            'jobs.tsv',
            dict(external_job_id='id', tool_id='tool_id',
                 tool_version='tool_version', state='state',
                 create_time='create_time'),
            static_mapping={
                'instance_id': instance.id,
            },
            delimiter='\t'
        )
        c.save()

        c = CopyMapping(
            JobParam,
            'params.tsv',
            dict(external_job_id='job_id', name='name', value='value'),
            static_mapping={
                'instance_id': instance.id,
            },
            delimiter='\t'
        )
        c.save()

        c = CopyMapping(
            MetricNumeric,
            'metric_num.tsv',
            dict(external_job_id='job_id',
                 plugin='plugin', name='name', value='value'),
            static_mapping={
                'instance_id': instance.id,
            },
            delimiter='\t'
        )
        c.save()

        c = CopyMapping(
            MetricText,
            'metric_txt.tsv',
            dict(external_job_id='job_id',
                 plugin='plugin', name='name', value='value'),
            static_mapping={
                'instance_id': instance.id,
            },
            delimiter='\t'
        )
        c.save()
        # instance.users_recent = meta['users']['active']
        # instance.users_total = meta['users']['total']
        # instance.jobs_run = meta['jobs']['ok']
        # instance.last_import = report_id
        # instance.save()
        # print("Update %s" % instance)
