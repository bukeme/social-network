import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import Thread, ChatMessage, ChatImageFrame

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		thread_pk = await self.get_thread_pk()
		# print(thread_pk)
		self.room_group_name = f'thread{thread_pk}'
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()

	async def receive(self, text_data):
		data_json = json.loads(text_data)
		chat_message_pk = data_json.get('chat_message_pk')
		chat_image_frame_pk = data_json.get('image_frame_pk')
		response = {'user': self.scope['user'].username}
		if chat_message_pk:
			chat_msg = await self.get_chat_message_text(pk=chat_message_pk)
			response['chat_message'] = chat_msg[0]
			response['date'] = chat_msg[1].strftime('%d/%m/%y %I:%H %p')
		if chat_image_frame_pk:
			chat_images = await self.get_chat_images(pk=chat_image_frame_pk)
			response['chat_images'] = chat_images[0]
			response['date'] = chat_images[1].strftime('%d/%m/%y %I:%H %p')
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'send_chat_data',
				'data': response
			}
		)

	async def send_chat_data(self, event):
		data = event['data']
		await self.send(text_data=json.dumps({'data': data}))

	async def disconnect(self, close_code):
		self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	@database_sync_to_async
	def get_thread_pk(self):
		other_user_pk = self.scope['url_route']['kwargs']['user_pk']
		user = self.scope['user']
		thread_pk = Thread.objects.get_or_new(user_pk=user.pk, other_user_pk=other_user_pk)[0].pk
		return thread_pk

	@database_sync_to_async
	def get_chat_message_text(self, pk):
		message = ChatMessage.objects.get(pk=int(pk))
		msg, date = message.message, message.created
		return [msg, date]

	@database_sync_to_async
	def get_chat_images(self, pk):
		image_frame = ChatImageFrame.objects.get(pk=int(pk))
		image_url_list = []
		for image in image_frame.chatimage_set.all():
			image_url_list.append(image.image.url)
		date = image_frame.created
		return [image_url_list, date]

	
