from django.http import JsonResponse
import psutil
def computational_resources(req):
    return JsonResponse({
        "cpu_utilized": psutil.cpu_percent(),
        "available mem": psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    })
