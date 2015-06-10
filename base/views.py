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
    res = 'galaxy-radio-telescope-%s' % ip
    expiry = 60 * 60 * 24 * 10
    # Stamps last TEN days.
    # TODO: decrease to 5 minutes
    import pprint; pprint.pprint("Expected res: %s" % res)
    return check(stamp, resource=res, check_expiration=expiry, bits=10)


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'uuid'

class GalaxyInstanceListView(ListView):
    model = GalaxyInstance
