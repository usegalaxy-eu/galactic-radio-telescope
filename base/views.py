""" Views for the base application """
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from .forms import ReportForm
from .models import GalaxyInstance
from .hashcash import check
import socket
if hasattr(socket, 'setdefaulttimeout'):
    socket.setdefaulttimeout(3)


@csrf_exempt
@transaction.atomic
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        import pprint; pprint.pprint(form.data)
        hashcash = form.data['hashcash']
        # TODO: form validation/cleaning
        # TODO: is this hashcash strong enough? Should we make them request a
        # "registration token" and hashcash that, and have those expire too?
        if _validate_hashcash(hashcash, request.META['REMOTE_ADDR']):
            # Do file processing
            try:
                gi = GalaxyInstance.objects.get(ipv4addr=form.data['ipaddr'])

                # Update instance metadata
                for attr in ('public', 'users_recent', 'users_active',
                             'users_total', 'jobs_run', 'humanname',
                             'description'):
                    if attr in form.data:
                        setattr(gi, attr, form.data[attr])
                # Save instance
                gi.save()
            except GalaxyInstance.DoesNotExist:
                dnsdomainname = socket.gethostbyaddr(form.data['ipaddr'])[0]
                kwargs = {
                    'ipv4addr': form.data['ipaddr'],
                    'dnsdomainname': dnsdomainname,
                }
                for attr in ('public', 'users_recent', 'users_active',
                             'users_total', 'jobs_run', 'humanname',
                             'description'):
                    kwargs[attr] = form.data[attr]

                gi = GalaxyInstance(**kwargs)
                gi.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse("Bad hashcash", status=400)
    else:
        form = ReportForm()
        return render(request, 'base/report.html', {'form': form})
        #return HttpResponse(status=400)


def _validate_hashcash(stamp, ip):
    res = _build_challenge(ip)
    expiry = 60 * 60 * 24 * 10
    # Stamps last TEN days.
    # TODO: decrease to 5 minutes
    return check(stamp, resource=res, check_expiration=expiry, bits=10)


@csrf_exempt
def report_challenge(request):
    return HttpResponse(_build_challenge(request), status=400)

def _build_challenge(request):
    """Hashcash challenges are per-site. I feel like I should further make this
    random/site specific, but I'm not even convinced that it really needs to be
    done?

    The goal is to disincentivise spamming GRT with bad data. Maybe as a result
    of this, for every error in parsing of your data, we ratchet the difficulty
    up until it's impossible to submit data? (Galaxy side would have a cutoff
    where it'd log an admin message to say "hey, something is seriously wrong
    here")

    Detecting bad data is tough..., so we're screwing over entire sites/IP
    addresses until we can get a solution for that.
    """
    ipaddr = request.META['REMOTE_ADDR']
    return 'galaxy-radio-telescope-%s' % ipaddr


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'uuid'

class GalaxyInstanceListView(ListView):
    model = GalaxyInstance
