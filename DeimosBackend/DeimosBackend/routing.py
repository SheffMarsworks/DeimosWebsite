from django.urls import re_path
from .consumers import TelemetryConsumer

websocket_urlpatterns = [
    re_path(r'ws/control/$', TelemetryConsumer.as_asgi()),
]
