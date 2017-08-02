from django.contrib.auth.models import User, Group
from rest_framework import serializers
from web.models import Tool, ToolVersion, GalaxyInstance


class GalaxyInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalaxyInstance
        fields = (
            'id', 'url', 'title', 'description', 'public', 'users_recent',
            'users_total', 'jobs_run', 'latitude', 'longitude', 'tools',
            'owners'
        )
