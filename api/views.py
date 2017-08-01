import json
import re
import os
import subprocess

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import GalaxyInstance


def compare(val1, val2):
    """
    Returns True if the two strings are equal, False otherwise.

    The time taken is independent of the number of characters that match.

    For the sake of simplicity, this function executes in constant time only
    when the two strings have the same length. It short-circuits when they
    have different lengths.

    From http://www.levigross.com/2014/02/07/constant-time-comparison-functions-in...-python-haskell-clojure-and-java/
    """
    if len(val1) != len(val2):
        return False

    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0


def authenticate(request):
    if request.method != 'POST':
        return HttpResponse(content='Must be a POST', status=405)

    auth_token = request.META.get('HTTP_AUTHORIZATION', None)
    if not auth_token:
        return HttpResponse('{"state": "error", "message": "Bad authentication credentials"}', status=400)

    gx_uuid, api_key = auth_token.split(':')
    # Find the Galaxy Instance with this username (uuid).
    try:
        galaxy = GalaxyInstance.objects.get(id=gx_uuid)
    except GalaxyInstance.DoesNotExist:
        return HttpResponse('{"state": "error", "message": "Bad authentication credentials"}', status=400)

    if not compare(str(galaxy.api_key), api_key):
        return HttpResponse('{"state": "error", "message": "Bad authentication credentials"}', status=400)

    return galaxy


# Create your views here.
@csrf_exempt
def whoami(request):
    galaxy = authenticate(request)
    if not isinstance(galaxy, GalaxyInstance):
        return galaxy

    return HttpResponse(
        content=json.dumps({
            'galaxy': galaxy.title,
            'uploaded_reports': galaxy.uploaded_reports()
        }),
        status=200
    )


@csrf_exempt
def v2_upload_data(request):
    """Accept uploaded data regarding jobs"""
    galaxy = authenticate(request)
    if not isinstance(galaxy, GalaxyInstance):
        return galaxy

    # We are permissive about uploads because we know we can go back and wipe
    # them out later / blacklist this instance if they're misbehaving. This is
    # further ameliorated by the fact that reports are not immediately public,
    # we process them offline. So this is not just a place people can dump
    # files and have them be web accessible.
    report_identifier = request.POST.get('identifier')

    if len(request.FILES.keys()) != 2 or 'data' not in request.FILES or 'meta' not in request.FILES:
        return HttpResponse('{"state": "error", "message": "Bad data"}', status=400)

    if not re.match(r'^[0-9.]+$', report_identifier):
        return HttpResponse('{"state": "error", "message": "Invalid report_identifier"}', status=400)


    meta_file = os.path.join(galaxy.report_dir, report_identifier + '.json')
    data_file = os.path.join(galaxy.report_dir, report_identifier + '.tsv.gz')

    with open(meta_file, 'wb+') as handle:
        for chunk in request.FILES['meta'].chunks():
            handle.write(chunk)

    with open(data_file, 'wb+') as handle:
        for chunk in request.FILES['data'].chunks():
            handle.write(chunk)

    # # We should also validate their upload.
    with open(meta_file, 'r') as handle:
        data = json.load(handle)
        report_hash = data['report_hash']
        algo, value = report_hash.split(':')
        if algo == 'sha256':
            real_value = subprocess.check_output(['sha256sum', data_file]).decode('utf-8')
            real_value = real_value[0:real_value.index(' ')]
            if value != real_value:
                os.unlink(data_file)
                os.unlink(meta_file)
                return HttpResponse(content='{"state": "error", "message": "Hash mismatch %s != %s"}' % (real_value, value), status=200)
        else:
            return HttpResponse(content='{"state": "error", "message": "Unsupported hash"}', status=200)

    # Otherwise, we're happy with what they've submitted.
    return HttpResponse(content='{"state": "success"}', status=200)
