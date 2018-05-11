import logging

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from api.models import GalaxyInstance
from registration.backends.simple.views import RegistrationView

log = logging.getLogger(__name__)


class GalaxyInstanceEdit(UpdateView):
    model = GalaxyInstance
    slug_field = 'id'
    fields = ('url', 'title', 'description')


class GalaxyInstanceView(DetailView):
    model = GalaxyInstance
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(GalaxyInstanceView, self).get_context_data(**kwargs)
        context['url'] = "{}://{}{}".format(request.scheme, request.get_host(), reverse_lazy('home'))
        return context


class GalaxyInstanceConfig(DetailView):
    model = GalaxyInstance
    slug_field = 'id'
    template_name_suffix = '.yml'


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
    fields = ('url', 'title', 'description')
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


class CustomRegistrationView(RegistrationView):

    def get_success_url(self, user):
        return reverse_lazy('home')
