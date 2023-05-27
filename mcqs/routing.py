from django.urls import path
from mcqs import consumers

websocket_urlpatterns = [
    path('timer/', consumers.TimerConsumer.as_asgi()),
]
