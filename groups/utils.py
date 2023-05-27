from groups.models import CustomGroup


def get_all_group_photos(group_pk):
	group = CustomGroup.objects.get(pk=group_pk)
	tmp1 = group.groupprofileimage_set.last().pk
	q1 = group.groupprofileimage_set.exclude(pk=tmp1)
	q2 = [img for post in group.post_set.all() for img in post.postimage_set.all()]
	q = [*q1, *q2]
	return sorted(q, key=lambda x: x.created, reverse=True)

def get_all_group_videos(group_pk):
	group = CustomGroup.objects.get(pk=group_pk)
	tmp = [post for post in group.post_set.all() if post.video]
	q = [post.video for post in sorted(tmp, key=lambda x: x.created, reverse=True)]
	return q