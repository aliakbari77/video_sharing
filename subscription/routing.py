from django.urls import re_path, path
from subscription.consumers import CommentConsumer, ViewerConsumer

websocket_urlpatterns = [
    path('ws/video/<int:video_id>/', CommentConsumer.as_asgi()),
    path('ws/video/viewer/<int:video_id>/', ViewerConsumer.as_asgi()),
]
