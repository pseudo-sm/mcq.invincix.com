from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
import asyncio
from datetime import timedelta
from asgiref.sync import sync_to_async

from . models import Candidate
class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()       
    
    @sync_to_async
    def get_users(self,registration_no):
        return Candidate.objects.get(registration_no=registration_no)
    
    @sync_to_async
    def candidate_deduct(self,registration_no):
        candidate = Candidate.objects.get(registration_no=registration_no)
        candidate.time = candidate.time-timedelta(seconds=1)
        candidate.save()
        return candidate
    
    async def receive(self,text_data):
        candidate = await self.candidate_deduct(text_data)
        delta = candidate.time
        h = delta.seconds // 3600
        m = (delta.seconds % 3600) // 60
        s = delta.seconds % 60
        await self.send(text_data= '{{"hours":{0}, "minutes":{1},"seconds":{2}}}'.format(h,m,s))
