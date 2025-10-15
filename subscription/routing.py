from django.urls import re_path
from subscription.consumers import CommentConsumer

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<video_id>\d+)/$', CommentConsumer.as_asgi()),
]
