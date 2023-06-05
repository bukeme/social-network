from chats.models import Thread


def get_thread_chat_data(thread_pk):
	thread = Thread.objects.get(pk=thread_pk)
	chat_messages = list(thread.chatmessage_set.all())
	chat_image_frames = list(thread.chatimageframe_set.all())
	chat_data = [*chat_messages, *chat_image_frames]
	return sorted(chat_data, key=lambda x: x.created)