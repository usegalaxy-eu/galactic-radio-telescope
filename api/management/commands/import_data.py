import json
import tarfile
import os
import uuid
import tempfile
import logging

from api.models import GalaxyInstance, Job, JobParam, MetricNumeric, MetricText, Dataset
from api.validator import validate

from django.core.management.base import BaseCommand
# from django.conf import settings
from django.db import transaction
# from django.contrib.auth.models import User
from postgres_copy import CopyMapping


logging.basicConfig(level=logging.DEBUG)
TMPDIR = os.path.join(tempfile.gettempdir(), 'grt')
if not os.path.exists(TMPDIR):
    os.makedirs(TMPDIR)


class Command(BaseCommand):
    help = 'Load all data from the report directory.'

    def handle(self, *args, **options):
        # report_dir = settings.GRT_UPLOAD_DIRECTORY
        for instance in GalaxyInstance.objects.all():
            try:
                with transaction.atomic():
                    for report_id in sorted(instance.new_reports()):
                        if not self.import_report(instance, report_id):
                            raise Exception("Import error")
                    # Once we've finished parsing reports for this instance, update the count.
                    instance.jobs_total = Job.objects.filter(instance_id=instance.id).count()
                    instance.save()
            except Exception as e:
                pass


    def fix_name(self, member):
        if '.jobs.tsv' in member.name:
            return 'jobs'
        elif '.metric_num.tsv' in member.name:
            return 'metric_num'
        elif '.params.tsv' in member.name:
            return 'params'
        elif '.datasets.tsv' in member.name:
            return 'datasets'
        return 'unknown'

    def import_report(self, instance, report_id):
        report_base = os.path.join(instance.report_dir, report_id)
        logging.info("[%s] Processing %s", instance.id, report_base)

        # first load the metadata
        with open(report_base + '.json', 'r') as handle:
            meta = json.load(handle)
            try:
                validate(meta)
            except Exception as e:
                logging.exception(e)
                return False

        # Next we'll extract files.
        extracted_files = []
        data_map = {}
        with tarfile.open(report_base + '.tar.gz', 'r') as tar:
            for member in tar:
                guessed = self.fix_name(member)
                if guessed == 'unknown':
                    continue

                # fancy safe name.
                tmpname = uuid.uuid4().hex + '.tsv'
                extracted_to = os.path.join(tempfile.gettempdir(), 'grt', tmpname)
                logging.info("[%s] Extracting %s to %s, guessed:%s", instance.id, member.name, extracted_to, guessed)
                # Record where the 'params' file is or the 'metrics' file.
                data_map[guessed] = extracted_to
                # Change the archive member's name in order to ensure that it
                # is extracted to somewhere with a safe name.
                member.name = tmpname
                # Extract into CWD.
                tar.extract(member, TMPDIR)
                # Track where we put it for cleanup later.
                extracted_files.append(extracted_to)

        if 'jobs' in data_map:
            c = CopyMapping(
                Job,
                data_map['jobs'],
                dict(external_job_id='id', tool_id='tool_id',
                    tool_version='tool_version', state='state',
                    create_time='create_time'),
                quote_character="\b",
                static_mapping={
                    'instance_id': instance.id,
                },
                delimiter='\t'
            )
            c.save()

        if 'params' in data_map:
            c = CopyMapping(
                JobParam,
                data_map['params'],
                dict(external_job_id='job_id', name='name', value='value'),
                quote_character="\b",
                static_mapping={
                    'instance_id': instance.id,
                },
                delimiter='\t'
            )
            c.save()

        if 'metric_num' in data_map:
            c = CopyMapping(
                MetricNumeric,
                data_map['metric_num'],
                dict(external_job_id='job_id',
                    plugin='plugin', name='name', value='value'),
                quote_character="\b",
                static_mapping={
                    'instance_id': instance.id,
                },
                delimiter='\t'
            )
            c.save()

        if 'datasets' in data_map:
            c = CopyMapping(
                Dataset,
                data_map['datasets'],
                dict(
                    external_job_id='job_id',
                    external_dataset_id='dataset_id',
                    extension='extension',
                    file_size='file_size',
                    param_name='param_name',
                    file_type='type',
                ),
                quote_character="\b",
                static_mapping={
                    'instance_id': instance.id,
                },
                delimiter='\t'
            )
            c.save()

        for f in extracted_files:
            try:
                logging.info("[%s] Cleaning up %s", instance.id, f)
                os.unlink(f)
            except Exception as e:
                logging.exception(e)

        if 'users' in meta:
            if 'active' in meta['users']:
                instance.users_recent = meta['users']['active']
            if 'total' in meta['users']:
                instance.users_total = meta['users']['total']
        if 'jobs' in meta:
            if 'ok' in meta['jobs']:
                instance.jobs_run = meta['jobs']['ok']

        instance.last_import = report_id
        instance.save()
        return True
