from django.urls import path, re_path

from communications.api.consumers.admin_chat_consumers import AdminChatConsumers

websocket_urlpatterns = [

    path('ws/communications/admin_chat', AdminChatConsumers.as_asgi()),

]