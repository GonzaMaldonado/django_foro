from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
  path('ws/<int:pk>/', ChatConsumer.as_asgi()),
]