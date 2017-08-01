from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from api import viewsets
from api import views

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'galaxies', viewsets.GalaxyInstanceViewSet, 'Galaxy')
router.register(r'tools', viewsets.ToolViewSet, 'Tool')

urlpatterns = [
    url('api/', include(router.urls, namespace="api")),
    url('api/whoami', views.whoami),
    url('api/v2/upload', views.v2_upload_data),
]
