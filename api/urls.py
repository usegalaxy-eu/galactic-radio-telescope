from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from .views import stats_galaxy, stats_jobs, v1_upload_data, \
    GalaxyInstanceView, \
    GalaxyInstanceEdit, \
    GalaxyInstanceCreate, \
    GalaxyInstanceCreateSuccess, \
    GalaxyInstanceListView, \
    GalaxyInstanceListCompareView, \
    OwnedGalaxyInstanceListView, \
    ToolView, ToolList

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base/home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^about.html', TemplateView.as_view(template_name='base/about.html')),
    url(r'^stats/jobs/$', stats_jobs, name='stats-jobs'),
    url(r'^galaxy/$', GalaxyInstanceListView.as_view(), name='galaxy-instance-list'),
    url(r'^galaxy/compare$', GalaxyInstanceListCompareView.as_view(), name='stats-galaxy'),
    url(r'^galaxy/create$', GalaxyInstanceCreate.as_view(), name='galaxy-instance-create'),
    url(r'^galaxy/(?P<slug>[0-9a-f-]{36})/$', GalaxyInstanceView.as_view(), name='galaxy-instance-detail'),
    url(r'^galaxy/(?P<slug>[0-9a-f-]{36})/edit$', GalaxyInstanceEdit.as_view(), name='galaxy-instance-edit'),
    url(r'^galaxy/(?P<slug>[0-9a-f-]{36})/success$', GalaxyInstanceCreateSuccess.as_view(), name='galaxy-instance-create-success'),
    url(r'^galaxy/owned$', OwnedGalaxyInstanceListView.as_view(), name='owned-galaxy-instance-list'),

    url(r'^tool/$', ToolList.as_view(), name='tool-list'),
    url(r'^tool/(?P<pk>[0-9a-f-]{36})/$', ToolView.as_view(), name='tool-detail'),

    url(r'^api/v1/upload$', v1_upload_data, name='v1-upload'),
    url(r"^account/", include("account.urls")),

]
