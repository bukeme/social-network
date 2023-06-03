from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import FriendRequest


def get_all_photos(request, user_pk):
	user = User.objects.get(pk=user_pk)
	userprofile = User.objects.get(pk=user_pk).userprofile
	posts = user.post_set.filter(
		Q(visibility='public') | Q(user=request.user)
	)
	tmp_pi = userprofile.profileimage_set.last().pk
	q1 = list(userprofile.profileimage_set.exclude(pk=tmp_pi))
	tmp_ci = userprofile.coverimage_set.last().pk
	q2 = list(userprofile.coverimage_set.exclude(pk=tmp_ci))
	q3 = [post_img for post in posts for post_img in post.postimage_set.all()]
	q = [*q1, *q2, *q3]
	return sorted(q, key=lambda x: x.created, reverse=True)

def get_friend_request_object(to_user_pk, from_user_pk):
	to_user = User.objects.get(pk=to_user_pk)
	from_user = User.objects.get(pk=from_user_pk)
	return FriendRequest.objects.get(to_user=to_user, from_user=from_user)

def get_user_post_feeds(request, user_pk):
	user = User.objects.get(pk=user_pk)
	posts = user.post_set.all()
	user_posts = posts.filter(group__isnull=True)
	group_posts = posts.filter(group__isnull=False)
	if request.user == user:
		return posts
	elif request.user in user.userprofile.followers.all() or request.user in user.userprofile.friends.all():
		q1 = user_posts.filter(Q(visibility='public') | Q(visibility='friends'))
		q2 = group_posts.filter(group__members__in=[request.user])
		q = q1.union(q2)
		return q
	else:
		q1 = user_posts.filter(visibility='public')
		q2 = group_posts.filter(group__members__in=[request.user])
		q = q1.union(q2)
		return q.order_by('-created')

def filter_user_queryset(queryset, query):
    result = []
    queryset = list(queryset)
    for user in queryset:
        if (query.lower() in user.userprofile.full_name.lower()) or (query.lower() in user.username.lower()):
            result.append(user)
    return result

# def filter_user_queryset(queryset, query):
# 	result = []
# 	queryset = list(queryset)
# 	for user in queryset:
# 	    if (query.lower() in user.userprofile.full_name.lower()) or (query.lower() in user.username.lower()):
# 	        result.append(user)
#     # return result