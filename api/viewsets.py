from rest_framework import viewsets, filters
from api.serializers import GalaxyInstanceSerializer
from api.models import GalaxyInstance


class GalaxyInstanceViewSet(viewsets.ModelViewSet):
    queryset = GalaxyInstance.objects.all()
    serializer_class = GalaxyInstanceSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('public',)
    ordering_fields = ('name',)
