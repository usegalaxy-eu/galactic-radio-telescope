from django.contrib import admin
from .models import GalaxyInstance, Job, Tool, ToolVersion

admin.site.register(GalaxyInstance)
admin.site.register(Job)
admin.site.register(Tool)
admin.site.register(ToolVersion)
