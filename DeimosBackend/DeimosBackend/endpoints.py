from django.http import JsonResponse
from rest_framework import status
import psutil
from .monitor_ros import list_ros_topic
def computational_resources(req):
    return JsonResponse({
        "cpu_utilized": psutil.cpu_percent(),
        "available mem": psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    })
def topiclist(req):
    all_topics = list_ros_topic()
    if len(all_topics) <= 2:
        return JsonResponse({
            "error_stat": "1",
            "error_msg": "Please start other ros process" 
        },status=425)
    else:
        return JsonResponse({
            "num_topic": len(all_topics),
            "data": all_topics
        },status=200)