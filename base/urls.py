"""urlconf for the base application"""

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from .views import GalaxyInstanceView
from .views import GalaxyInstanceListView

urlpatterns = patterns('base.views',
    url(r'^$', TemplateView.as_view(template_name='base/home.html'), name='home'),
    url(r'^about.html', TemplateView.as_view(template_name='base/about.html')),
    url(r'^report/$', 'report'),
    url(r'^report/challenge/$', 'report_challenge'),
    url(r'^galaxy/$', GalaxyInstanceListView.as_view(), name='galaxy-instance-list'),
    url(r'^galaxy/(?P<slug>[0-9a-f]{32})/$', GalaxyInstanceView.as_view(), name='galaxy-instance-detail'),
)
