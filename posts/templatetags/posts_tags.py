from django import template
from posts.models import Post
from chats.models import Thread

register = template.Library()


@register.simple_tag
def post_imgs(post):
	return post.postimage_set.all()[:3]

@register.inclusion_tag('posts/right-section.html')
def chats(user_pk):
	return {'user_threads': Thread.objects.get_thread_users(user_pk)[:10]}