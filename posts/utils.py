from posts.models import Post
from django.db.models import Q


def get_feeds_queryset(request):
	q = []
	q1 = Post.objects.filter(
		Q(visibility='public') | Q(user=request.user)
	)
	# q2 = SharedPost.objects.filter(
	# 	Q(visibility='public') | Q(user=request.user)
	# )
	q.extend(list(q1))
	# q.extend(list(q2))
	print(q)
	return q