import json
from channels.generic.websocket import AsyncWebsocketConsumer
from subscription.models import Comment, Video, WatchHistory
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.room_group_name = f'video_{self.video_id}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_comment(username, self.video_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'message': message,
                'username': username,
            }
        )

    async def comment_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @sync_to_async
    def save_comment(self, username, video_id, message):
        user = User.objects.get(username=username)
        video = Video.objects.get(id=video_id)
        Comment.objects.create(user=user, video=video, content=message)


class ViewerConsumer(AsyncWebsocketConsumer):  
    async def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['video_id']
        self.room_group_name = f'video_{self.video_id}_viewer'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data['username']

        created_new_viewer = await self.save_viewer(username, self.video_id)

        if created_new_viewer:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'update_viewer',
                    'username': username,
                }
            )

    async def update_viewer(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({
            'username': username
        }))
    
    @sync_to_async
    def save_viewer(self, username, video_id):
        user = User.objects.get(username=username)
        video = Video.objects.get(id=video_id)
        watch_history, created = WatchHistory.objects.get_or_create(user=user, video=video)
        return created

