import json
import logging

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .models import GalaxyInstance, Tool, Job

log = logging.getLogger(__name__)


class GalaxyInstanceEdit(UpdateView):
    model = GalaxyInstance
    slug_field = 'uuid'
    fields = ('url', 'humanname', 'description', 'public', 'latitude', 'longitude', 'tags')


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(GalaxyInstanceView, self).get_context_data(**kwargs)
        context['recent_jobs'] = Job.objects.all().filter(instance=context['object']).order_by('-date')[0:10]
        return context


class GalaxyInstanceCreateSuccess(DetailView):
    model = GalaxyInstance
    slug_field = 'uuid'
    template_name_suffix = '_create_success'

    def get_context_data(self, **kwargs):
        context = super(GalaxyInstanceCreateSuccess, self).get_context_data(**kwargs)
        full_url = self.request.build_absolute_uri(str(reverse_lazy('galaxy-instance-create-success', args=(self.object.uuid, ))))
        components = full_url.split('/')[0:-3] + ['api', 'v1', 'upload']
        context['api_url'] = '/'.join(components)
        return context


class GalaxyInstanceCreate(CreateView):
    model = GalaxyInstance
    fields = ('url', 'humanname', 'description', 'public', 'latitude', 'longitude', 'tags')
    template_name_suffix = '_create'

    def get_success_url(self):
        return reverse_lazy(
            'galaxy-instance-create-success',
            kwargs={'slug': self.object.uuid}
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class GalaxyInstanceListView(ListView):
    model = GalaxyInstance


class TaggedGalaxyInstanceListView(ListView):
    model = GalaxyInstance
    template_name_suffix = '_list'

    def get_context_data(self, **kwargs):
        context = super(TaggedGalaxyInstanceListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        import pprint; pprint.pprint(context)
        return context

    def get_queryset(self):
        return GalaxyInstance.objects.filter(tags=self.kwargs['slug'])


class OwnedGalaxyInstanceListView(ListView):
    model = GalaxyInstance

    def get_queryset(self):
        return GalaxyInstance.objects.filter(owner=self.request.user)


class ToolView(DetailView):
    model = Tool
    slug_field = 'id'


class ToolList(ListView):
    model = Tool

    def get_context_data(self, **kwargs):
        context = super(ToolList, self).get_context_data(**kwargs)
        paginator = Paginator(self.object_list, 25)

        page = self.request.GET.get('page')

        try:
            page_objects = paginator.page(page)
        except PageNotAnInteger:
            page_objects = paginator.page(1)
        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context['objects'] = page_objects
        return context


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


def galaxy_geojson(request, pk=None):
    if pk is not None:
        galaxies = [GalaxyInstance.objects.get(uuid=pk)]
    else:
        galaxies = GalaxyInstance.objects.all()

    data = {
        "type": "FeatureCollection",
        "features": []
    }

    for galaxy in galaxies:
        if galaxy.public or request.user == galaxy.owner or request.user.is_superuser:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [ galaxy.longitude, galaxy.latitude ],
                },
                'properties': {
                    'name': galaxy.humanname,
                    'url': galaxy.url,
                    'description': galaxy.description,
                    'id': str(galaxy.uuid),
                    'tags': [str(x) for x in galaxy.tags.all()],
                }
            }

            if 'university' in galaxy.tags:
                feature['properties'].update({
                    'class': 'college',
                })

            data['features'].append(feature)

    return HttpResponse(content=json.dumps(data), status=200)
