from django import template
from django.forms.models import model_to_dict
from accounts.models import FriendRequest
from django.db.models import Q

register = template.Library()

@register.filter(name='fieldvalue')
def fieldvalue(model, field):
	model_dict = model_to_dict(model)
	return model_dict[field]

@register.simple_tag
def define(value=None):
	return value 

@register.simple_tag
def sent_friend_request(to_user, from_user):
	return FriendRequest.objects.filter(
		Q(to_user=to_user) & Q(from_user=from_user)
	).exists()

@register.simple_tag
def friend_request_count(user):
	return FriendRequest.objects.filter(
		to_user=user
	).count()