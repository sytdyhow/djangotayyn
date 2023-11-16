# from djangochannelsrestframework import permissions
# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import ListModelMixin
# from djangochannelsrestframework.observer import model_observer

# from .models import  Filterlog
# from .serializers import AllFilterLogSerializer


# class PostConsumer(ListModelMixin, GenericAsyncAPIConsumer):

#     queryset = Filterlog.objects.all()
#     serializer_class = AllFilterLogSerializer
#     permissions = (permissions.AllowAny,)

#     async def connect(self, **kwargs):
#         await self.model_change.subscribe()
#         await super().connect()

#     @model_observer(Filterlog)
#     async def model_change(self, message, observer=None, **kwargs):
#         await self.send_json(message)

#     @model_change.serializer
#     def model_serialize(self, instance, action, **kwargs):
#         return dict(data=AllFilterLogSerializer(instance=instance).data, action=action.value)
import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            
        )
        print(self.room_group_name,"groupname")
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
        
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        

class JokesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('countdata',self.channel_name)
        await self.accept()
        
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard('countdata',self.channel_name)
   
    async def send_data(self,event):
        text_message = event['text']
        text_mes = json.dumps(text_message)
        await self.send(text_mes)