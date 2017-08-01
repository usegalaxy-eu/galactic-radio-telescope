import logging

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import GalaxyInstance, Tool, Job

log = logging.getLogger(__name__)


class GalaxyInstanceEdit(UpdateView):
    model = GalaxyInstance
    slug_field = 'id'
    fields = ('url', 'title', 'description', 'public', 'latitude', 'longitude')


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(GalaxyInstanceView, self).get_context_data(**kwargs)
        context['recent_jobs'] = Job.objects.all().filter(instance=context['object']).order_by('-date')[0:10]
        return context


class GalaxyInstanceCreateSuccess(DetailView):
    model = GalaxyInstance
    slug_field = 'id'
    template_name_suffix = '_create_success'

    def get_context_data(self, **kwargs):
        context = super(GalaxyInstanceCreateSuccess, self).get_context_data(**kwargs)
        full_url = self.request.build_absolute_uri(str(reverse_lazy('galaxy-instance-create-success', args=(self.object.id, ))))
        components = full_url.split('/')[0:-3] + ['api', 'v1', 'upload']
        context['api_url'] = '/'.join(components)
        return context


class GalaxyInstanceCreate(CreateView):
    model = GalaxyInstance
    fields = ('url', 'title', 'description', 'public', 'latitude', 'longitude')
    template_name_suffix = '_create'

    def get_success_url(self):
        return reverse_lazy(
            'galaxy-instance-create-success',
            kwargs={'slug': self.object.id}
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.owners.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class GalaxyInstanceListView(ListView):
    model = GalaxyInstance


class TaggedGalaxyInstanceListView(ListView):
    model = GalaxyInstance
    template_name_suffix = '_list'

    def get_context_data(self, **kwargs):
        context = super(TaggedGalaxyInstanceListView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

    def get_queryset(self):
        return GalaxyInstance.objects.filter(tags=self.kwargs['slug'])


class OwnedGalaxyInstanceListView(ListView):
    model = GalaxyInstance

    def get_queryset(self):
        return GalaxyInstance.objects.filter(owners__in=[self.request.user])


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
