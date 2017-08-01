from django.contrib.auth.models import User, Group
from rest_framework import serializers
from web.models import Tool, ToolVersion, GalaxyInstance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # def create(self, validated_data):
        # user = User.objects.create(
            # username=validated_data['username'],
            # email = validated_data['email'],
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        # return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        write_only_fields = ('password',)


class ToolVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolVersion
        fields = ('version', )


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ('tool_id', 'tool_name', 'tool_version_set')


class GalaxyInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalaxyInstance
        fields = (
            'id', 'url', 'title', 'description', 'public', 'users_recent',
            'users_total', 'jobs_run', 'latitude', 'longitude', 'tools',
            'owners'
        )
