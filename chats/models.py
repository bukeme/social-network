from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User


# User = settings.AUTH_USER_MODEL

# Create your models here.

class ThreadManager(models.Manager):
	def get_or_new(self, user_pk, other_user_pk):
		if user_pk == other_user_pk:
			return None, False
		q1 = Q(first_id=user_pk) & Q(second_id=other_user_pk)
		q2 = Q(first_id=other_user_pk) & Q(second_id=user_pk)
		q = self.get_queryset().filter(q1 | q2)

		if q.count() == 1:
			return q.first(), False
		elif q.count() > 1:
			return q.order_by('created').first(), False
		elif not q.exists():
			user = User.objects.get(pk=user_pk)
			other_user = User.objects.get(pk=other_user_pk)
			obj = self.model(first=user, second=other_user)
			obj.save()
			return obj, True
		return None, False

	def get_thread_users(self, user_pk):
		qs = super().get_queryset().filter(
			Q(first_id=user_pk) | Q(second_id=user_pk)
		).order_by('-updated')
		user = User.objects.get(pk=user_pk)
		thread_users = [t.second if t.first.pk == user_pk else t.first for t in qs]
		for f in user.userprofile.friends.all():
			if f not in thread_users and f.pk != user_pk:
				thread_users.append(f)
		return thread_users


class Thread(models.Model):
	first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(default=timezone.now)

	objects = ThreadManager()


class ChatMessage(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	message = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		self.thread.updated = timezone.now
		self.thread.save()
		return super(ChatMessage, self).save(*args, **kwargs)

class ChatImageFrame(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

class ChatImage(models.Model):
	frame = models.ForeignKey(ChatImageFrame, on_delete=models.Model)
	image = models.ImageField(upload_to='chat_images/%Y-%m-%d')
	created = models.DateTimeField(auto_now_add=True)


