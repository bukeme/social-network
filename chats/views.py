from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from chats.models import Thread
from django.contrib.auth.models import User
from django.http import JsonResponse
from posts.decorators import AjaxRequiredOnlyMixin
from chats.models import Thread, ChatImageFrame, ChatImage, ChatMessage
from chats.utils import get_thread_chat_data

# Create your views here.

class ThreadView(LoginRequiredMixin, TemplateView):
	template_name = 'chats/thread.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['page'] = 'thread'
		return context

thread_view = ThreadView.as_view()

class ThreadChatView(LoginRequiredMixin, TemplateView):
	template_name = 'chats/thread_chat.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user_pk = kwargs['user_pk']
		thread, created = Thread.objects.get_or_new(user_pk=self.request.user.pk, other_user_pk=user_pk)
		thread.seen_chat_message(self.request.user.pk)
		context['thread'] = thread
		context['chat_user'] = User.objects.get(pk=user_pk)
		context['thread_data'] = thread.get_chat_data()
		return context 

thread_chat_view = ThreadChatView.as_view()

class ChatCreateView(AjaxRequiredOnlyMixin ,View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'not logged in'})
		response = {'status': 'success'}
		message = request.POST.get('message')
		images = request.FILES.getlist('chat-image')
		thread = Thread.objects.get(pk=kwargs['thread_pk'])
		if message:
			chat_message = ChatMessage.objects.create(user=request.user, thread=thread, message=message)
			response['chat_message_pk'] = chat_message.pk
		if images:
			image_frame = ChatImageFrame.objects.create(user=request.user, thread=thread)
			for image in images:
				ChatImage.objects.create(frame=image_frame, image=image)
			response['image_frame_pk'] = image_frame.pk

		return JsonResponse(response)

chat_create_view = ChatCreateView.as_view()

