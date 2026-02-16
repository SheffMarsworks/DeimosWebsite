import roslibpy
import subprocess
from django.utils import timezone
#from DeimosBackend.models import TopicHealth

def perform_ros_check():
    """
    Connects to ROS Bridge, checks all topics, and updates the DB.
    Returns: (bool success, str message)
    """
    client = roslibpy.Ros(host='localhost', port=9090)
    
    try:
        # 1. Connect with a short timeout (don't hang the API if ROS is down)
        client.run(timeout=3)
    except Exception:
        return False, "Could not connect to ROS Bridge (Is it running?)"

    # 2. Prepare the service call
    service = roslibpy.Service(client, '/rosapi/publishers', 'rosapi/Publishers')
    topics = TopicHealth.objects.all()

    updates = 0
    
    for topic in topics:
        try:
            request = roslibpy.ServiceRequest({'topic': topic.name})
            # Call the service (blocking)
            response = service.call(request)
            
            # Check if anyone is publishing
            publishers = response.get('publishers', [])
            topic.is_online = len(publishers) > 0
            topic.last_checked = timezone.now()
            topic.save()
            updates += 1
        except Exception:
            # If a specific topic check fails, mark it offline or log it
            topic.is_online = False
            topic.save()

    client.terminate()
    return True, f"Successfully refreshed {updates} topics."
def list_ros_topic():
    try:
        # Run 'ros2 topic list' command
        result = subprocess.run(
            ['ros2', 'topic', 'list'], 
            capture_output=True, 
            text=True
        )
        
        # Split the output by newlines to get a list
        topics = result.stdout.strip().split('\n')
        return topics
        
    except FileNotFoundError:
        return ["Error: ROS 2 environment not sourced or installed"]
def start_process(start_cmd):
    print(start_cmd)
    try:
        result = subprocess.Popen(
            start_cmd, #Spawn process in background
            shell=True,
        )
        return "Start Success"
    except FileNotFoundError:
        return "Invalid node name"

