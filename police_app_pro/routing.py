from django.urls import path, re_path

from chat.consumers import ChatConsumer
from communications.api.consumers.admin_chat_consumers import AdminChatConsumers

websocket_urlpatterns = [

    path('ws/communications/admin_chat', AdminChatConsumers.as_asgi()),

    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),

]