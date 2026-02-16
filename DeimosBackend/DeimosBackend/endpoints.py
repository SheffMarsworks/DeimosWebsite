from django.http import JsonResponse
from rest_framework import status
import psutil
from .monitor_ros import list_ros_topic,start_process
from django.views.decorators.csrf import csrf_exempt
def computational_resources(req):
    return JsonResponse({
        "cpu_utilized": psutil.cpu_percent(),
        "available mem": psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    })
@csrf_exempt
def topiclist(req):
    all_topics = list_ros_topic()
    if req.method == 'GET':
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
    elif req.method == 'POST':
        http_stat = 200
        node_name = req.POST.get('node_name')
        args = req.POST.get('args')
        start_cmd = "ros2 run "+node_name+" "+args+" &"
        start_status = start_process(start_cmd)
        if start_status == "Invalid node name":
            http_stat = 500
        return JsonResponse({
            "status_msgs": start_status
        },status=http_stat)