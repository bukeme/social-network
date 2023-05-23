from django import template
from posts.models import Post

register = template.Library()


@register.simple_tag
def post_imgs(post):
	return post.postimage_set.all()[:3]

@register.inclusion_tag('posts/right-section.html', takes_context=True)
def chats(context):
	return {}