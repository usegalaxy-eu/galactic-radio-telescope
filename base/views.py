""" Views for the base application """
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from .forms import ReportForm


@csrf_exempt
@transaction.atomic
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        hashcash = form.data['hashcash']

        if _validate_hashcash(hashcash):
            # Do file processing
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)


def _validate_hashcash(hashcash):
    return True
