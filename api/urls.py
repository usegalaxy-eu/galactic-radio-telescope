from django.conf.urls import url, patterns, include
from django.views.generic import TemplateView
from .views import GalaxyInstanceView, GalaxyInstanceListView, stats_galaxy, stats_jobs, report
from .views import GalaxyInstanceView
from .views import GalaxyInstanceListView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base/home.html'), name='home'),
    url(r'^about.html', TemplateView.as_view(template_name='base/about.html')),
    url(r'^report/$', report),
    url(r'^stats/galaxy/$', stats_galaxy, name='stats-galaxy'),
    url(r'^stats/jobs/$', stats_jobs, name='stats-jobs'),
    url(r'^galaxy/$', GalaxyInstanceListView.as_view(), name='galaxy-instance-list'),
    url(r'^galaxy/(?P<slug>[0-9a-f]{32})/$', GalaxyInstanceView.as_view(), name='galaxy-instance-detail'),
    url(r"^account/", include("account.urls")),
]
