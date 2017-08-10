from django.conf import settings

def url_prefix(request):
    return {'URL_PREFIX': settings.URL_PREFIX}
