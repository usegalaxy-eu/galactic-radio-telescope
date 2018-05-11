from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from .views import \
    GalaxyInstanceView, \
    GalaxyInstanceEdit, \
    GalaxyInstanceCreate, \
    GalaxyInstanceCreateSuccess, \
    GalaxyInstanceListView, \
    GalaxyInstanceConfig, \
    CustomRegistrationView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base/home.html'), name='home'),
    url(r'^privacy/$', TemplateView.as_view(template_name='base/privacy.html'), name='privacy'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^accounts/', include([
        url(r'^register/$',
                    CustomRegistrationView.as_view(),
                    name='registration_register'),
        url(r'', include('registration.auth_urls')),
    ])),
    url(r'^galaxy/$', GalaxyInstanceListView.as_view(), name='galaxy-instance-list'),
    url(r'^galaxy/create$', GalaxyInstanceCreate.as_view(), name='galaxy-instance-create'),

    url(r'^galaxy/(?P<slug>[0-9]+)/$', GalaxyInstanceView.as_view(), name='galaxy-instance-detail'),
    url(r'^galaxy/(?P<slug>[0-9]+)/edit$', GalaxyInstanceEdit.as_view(), name='galaxy-instance-edit'),
    url(r'^galaxy/(?P<slug>[0-9]+)/grt.yml$', GalaxyInstanceConfig.as_view(), name='galaxy-instance-config'),
    url(r'^galaxy/(?P<slug>[0-9]+)/success$', GalaxyInstanceCreateSuccess.as_view(), name='galaxy-instance-create-success'),
]
