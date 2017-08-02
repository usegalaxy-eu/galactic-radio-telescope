from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base/home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
