from django.contrib import admin
from .models import GalaxyInstance, Job, Tool, ToolVersion, JobParam, Metric

admin.site.register(Tool)
admin.site.register(ToolVersion)
admin.site.register(GalaxyInstance)
admin.site.register(Metric)
admin.site.register(JobParam)
admin.site.register(Job)
