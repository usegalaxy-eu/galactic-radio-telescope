from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def compare(val1, val2):
    """
    Returns True if the two strings are equal, False otherwise.

    The time taken is independent of the number of characters that match.

    For the sake of simplicity, this function executes in constant time only
    when the two strings have the same length. It short-circuits when they
    have different lengths.

    From http://www.levigross.com/2014/02/07/constant-time-comparison-functions-in...-python-haskell-clojure-and-java/
    """
    if len(val1) != len(val2):
        return False

    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0


# Create your views here.
@csrf_exempt
def whoami(request):
    print(request.META)
    # username = request.META.get('X_USERNAME')
    # api_key = request.META.get('')
    pass


@csrf_exempt
def v2_upload_data(request):
    """Accept uploaded data regarding jobs"""
    # Must be a POST
    if request.method != 'POST':
        return HttpResponse(content='Must be a POST', status=405)

    # Instance UUID must be available
    #instance_uuid = metadata.get('uuid', None)
    #if instance_uuid is None:
        #return HttpResponse('No instance UUID provided', status=400)

    #instance = get_object_or_404(GalaxyInstance, uuid=instance_uuid)

    ## Instance API key must be available
    #instance_api_key = metadata.get('api_key', None)
    #if instance_api_key is None:
        #return HttpResponse('No instance API key provided', status=400)

    ## Instance API key must be correct.
    #if not compare(str(instance_api_key), str(instance.api_key)):
        #return HttpResponse(status=403)

    ## First update Galaxy instance metadata
    #instance_users_recent = IntegerDataPoint(value=metadata.get('active_users', 0))
    #instance_users_recent.save()
    #instance.users_recent.add(instance_users_recent)

    #instance_users_total = IntegerDataPoint(value=metadata.get('total_users', 0))
    #instance_users_total.save()
    #instance.users_total.add(instance_users_total)

    #instance_jobs_run = IntegerDataPoint(value=metadata.get('recent_jobs', 0))
    #instance_jobs_run.save()
    #instance.jobs_run.add(instance_jobs_run)

    #instance.version = metadata.get('galaxy_version', 'Unknown')
    ##instance.tags = metadata.get('tags', [])
    ##if 'public' in instance.tags:
        ##instance.public = True
    ##else:
        ##instance.public = False
    #instance.description = metadata.get('description', '').strip()
    #instance.title = metadata.get('name', 'A Galaxy Instance')
    #if len(metadata.get('url', '').strip()) > 0:
        #instance.url = metadata['url']
    #else:
        #instance.url = None
    #instance.norm_users_recent = metadata.get('active_users', 0)

    #location = metadata.get('location', {'lat': 0, 'lon': 0})
    #instance.latitude = location.get('lat', 0)
    #instance.longitude = location.get('lon', 0)

    #instance.save()

    #tools = {}
    ## Next we process the acknowleged tools:
    #for idx, unsafe_tool_data in enumerate(data.get('tools', [])):
        ## 'tool_id': 'xmfa2tbl',
        ## 'tool_version': '2.4.0.0',
        ## 'tool_name': 'Convert XMFA to a percent identity table',
        #tool_data = {
            #'tool_id': unsafe_tool_data.get('tool_id', None),
            #'tool_version': unsafe_tool_data.get('tool_version', None),
            #'tool_name': unsafe_tool_data.get('tool_name', None)
        #}
        #for key in tool_data.keys():
            #if tool_data[key] is not None:
                #sanitized_value = re.sub('[^A-Za-z0-9_./ -]+', '', tool_data[key])
                #if tool_data[key] != sanitized_value:
                    #log.warn("Sanitizied %s from %s to %s", key, tool_data[key], sanitized_value)
                #tool_data[key] = sanitized_value
            #else:
                #tool_data[key] = ""

        ## Tool data is now theoretically safe.
        #tool, tool_created = Tool.objects.get_or_create(
            #tool_id=tool_data['tool_id'],
            #tool_name=tool_data['tool_name']
        #)
        #tool_version, tv_created = ToolVersion.objects.get_or_create(
            #tool=tool,
            #version=tool_data['tool_version']
        #)

        #tools[idx] = tool_version

    ## Now we need to process the list of new jobs sent to us by the
    ## client.
    #for unsafe_job_data in data.get('jobs', []):
        ## Will throw an error on bad data, which is OK.
        #tool_idx = int(unsafe_job_data.get('tool', 0))
        #if tool_idx not in tools:
            #return HttpResponse(content='Unknown tool id %s' % tool_idx, status=400)
        #else:
            #tool = tools[tool_idx]

        #job_date = int(unsafe_job_data.get('date', 0))

        #metrics = unsafe_job_data.get('metrics', {})

        #job = Job(
            #instance=instance,
            #tool=tool,
            #date=datetime.datetime.fromtimestamp(job_date),
            #metrics_core_runtime_seconds=int(metrics.get('core_runtime_seconds', 0)),
            #metrics_core_galaxy_slots=int(metrics.get('core_galaxy_slots', 0)),
        #)
        #job.save()

    #return HttpResponse(status=200)


