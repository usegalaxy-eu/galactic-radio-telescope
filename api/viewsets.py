from rest_framework import viewsets, filters, permissions, serializers
from django.contrib.auth.models import User, Group
from api.serializers import UserSerializer, ToolSerializer, ToolVersionSerializer, GalaxyInstanceSerializer
from web.models import User, Tool, ToolVersion, GalaxyInstance
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class GalaxyInstanceViewSet(viewsets.ModelViewSet):
    queryset = GalaxyInstance.objects.all()
    serializer_class = GalaxyInstanceSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('public',)
    ordering_fields = ('name',)


class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('tool_id',)
    ordering_fields = ('tool_id',)
