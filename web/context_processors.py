from django.conf import settings


cached_data = {
    'URL_PREFIX': settings.URL_PREFIX,
    'APP_VERSION': settings.GRT_VERSION,
    'GIT_REVISION': settings.RAVEN_CONFIG.get('release', None),
}

def url_prefix(request):
    return cached_data
