from django import template
from django.db.models import Q
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
	return {'thread_users': queryset, 'page': context.get('page'), 'chat_user': context.get('chat_user'), 'request': request}

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

# @register.simple_tag
# def user_threads(user_pk):
# 	return Thread.objects.get_thread_users(user_pk)

@register.simple_tag
def thread_unseen_chat_count(user_pk, other_user_pk):
	qs = Thread.objects.filter(
		(Q(first_id=user_pk) & Q(second_id=other_user_pk)) |
		(Q(first_id=other_user_pk) & Q(second_id=user_pk))
	)
	if qs.exists():
		return qs.first().unseen_chat_count(user_pk)
	else:
		return None

@register.simple_tag
def user_unseen_chat_count(user_pk):
	return Thread.objects.total_unseen_chat_count(user_pk)
    