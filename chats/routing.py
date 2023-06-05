from django.urls import re_path
from chats import consumers

websocket_urlpatterns = [
	re_path(r"ws/chats/(?P<user_pk>\w+)/$", consumers.ChatConsumer.as_asgi()),
]