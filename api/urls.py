from django.conf.urls import url, patterns, include
from django.views.generic import TemplateView
from .views import stats_galaxy, stats_jobs, v1_upload_data
from .views import GalaxyInstanceView
from .views import GalaxyInstanceEdit
from .views import GalaxyInstanceListView
from .views import OwnedGalaxyInstanceListView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base/home.html'), name='home'),
    url(r'^about.html', TemplateView.as_view(template_name='base/about.html')),
    url(r'^stats/galaxy/$', stats_galaxy, name='stats-galaxy'),
    url(r'^stats/jobs/$', stats_jobs, name='stats-jobs'),
    url(r'^galaxy/$', GalaxyInstanceListView.as_view(), name='galaxy-instance-list'),
    url(r'^galaxy/(?P<slug>[0-9a-f-]{36})/$', GalaxyInstanceView.as_view(), name='galaxy-instance-detail'),
    url(r'^galaxy/(?P<slug>[0-9a-f-]{36})/edit$', GalaxyInstanceEdit.as_view(), name='galaxy-instance-edit'),
    url(r'^galaxy/owned$', OwnedGalaxyInstanceListView.as_view(), name='owned-galaxy-instance-list'),
    url(r'^api/v1/upload$', v1_upload_data, name='v1-upload'),
    url(r"^account/", include("account.urls")),
]
