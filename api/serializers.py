from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import GalaxyInstance


class GalaxyInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalaxyInstance
        fields = (
            'id', 'url', 'title', 'description', 'public', 'users_recent',
            'users_total', 'jobs_run', 'latitude', 'longitude', 'tools',
            'owners'
        )
