from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import transaction
from .forms import ReportForm
from .models import GalaxyInstance
import socket
if hasattr(socket, 'setdefaulttimeout'):
    socket.setdefaulttimeout(3)


@csrf_exempt
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        dnsdomainname = socket.gethostbyaddr(form.data['ipaddr'])[0]

        try:
            gi = GalaxyInstance.objects.get(dnsdomainname=dnsdomainname)

            # Update instance metadata
            for attr in ('public', 'users_recent', 'users_total', 'jobs_run',
                        'humanname', 'description'):
                if attr in form.data:
                    setattr(gi, attr, form.data[attr])
            # Save instance
            gi.save()
        except GalaxyInstance.DoesNotExist:
            kwargs = {
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
        form = ReportForm()
        return render(request, 'base/report.html', {'form': form})


def stats_galaxy(request):
    userdata = {
        'x': ['<10', '10-49', '50-99', '100-199', '200-499', '500+'],
        'y1': [7, 8, 4, 4, 1, 1],
    }
    computedata = {
        'x': ['Standalone server', 'Compute cluster', 'Cloud'],
        'y1': [12, 10, 4],
    }
    storagedata = {
        'x': [x + ' Tb' for x in ['<10', '10-49', '50-99', '100-199', '200-299']],
        'y1': [8, 7, 4, 1, 4],
    }
    data = {
        'usertype': 'discreteBarChart',
        'userdata': userdata,
        'computetype': 'discreteBarChart',
        'computedata': computedata,
        'storagetype': 'discreteBarChart',
        'storagedata': storagedata,
    }
    return render(request, 'base/galaxy-stats.html', data)


def stats_jobs(request):
    xdata = ['0-10', '10-50', '50-100', '100-1000', '1000+']
    ydata = [1000, 200, 50, 10, 2]
    chartdata = {
        'x': xdata,
        'y1': ydata,
    }
    data = {
        'charttype': 'discreteBarChart',
        'chartdata': chartdata,
    }
    return render(request, 'base/galaxy-stats.html', data)


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'uuid'

class GalaxyInstanceListView(ListView):
    model = GalaxyInstance
