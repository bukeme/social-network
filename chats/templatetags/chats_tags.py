from django import template
from chats.models import Thread
from accounts.utils import filter_user_queryset

register = template.Library()

@register.inclusion_tag('chats/threadlist.html', takes_context=True)
def thread_list(context):
	request = context['request']
	query = request.GET.get('search-chat')
	user = request.user
	if query:
		queryset = filter_user_queryset(queryset=Thread.objects.get_thread_users(user.pk), query=query)
	else:
		queryset = Thread.objects.get_thread_users(user.pk)
	return {'thread_users': queryset, 'page': context.get('page'), 'chat_user': context.get('chat_user')}

@register.inclusion_tag('chats/mobile_threadlist.html', takes_context=True)
def mobile_thread_list(context):
	request = context['request']
	query = request.GET.get('search-chat')
	user = request.user
	if query:
		queryset = filter_user_queryset(queryset=Thread.objects.get_thread_users(user.pk), query=query)
	else:
		queryset = Thread.objects.get_thread_users(user.pk)
	return {'thread_users': queryset, 'chat_user': context.get('chat_user')}
    