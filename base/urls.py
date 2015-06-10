"""urlconf for the base application"""

from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('base.views',
    url(r'^$', TemplateView.as_view(template_name='base/home.html')),
    url(r'^about.html', TemplateView.as_view(template_name='base/about.html')),
    url(r'^report/$', 'report'),
)
