from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from api import viewsets as views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'galaxies', views.GalaxyInstanceViewSet, 'Galaxy')
router.register(r'tools', views.ToolViewSet, 'Tool')

urlpatterns = [
    url('api/', include(router.urls, namespace="api")),
]
