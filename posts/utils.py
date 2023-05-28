from posts.models import Post
from django.db.models import Q


def get_feeds_queryset(request):
	posts = Post.objects.all()
	group_posts = posts.filter(group__isnull=False)
	user_posts = posts.filter(group__isnull=True)
	q1 = user_posts.filter(
		Q(visibility='public') |
		Q(user__pk=request.user.pk) |
		(Q(visibility='friends') &
		(Q(user__userprofile__followers__in=[request.user]) |
		Q(user__userprofile__friends__in=[request.user])))
	)
	q2 = group_posts.filter(group__members__in=[request.user])

	q = q1.union(q2)
	return q.order_by('-created')