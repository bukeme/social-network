from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	other_name = models.CharField(max_length=200, null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	occupation = models.CharField(max_length=200, null=True, blank=True)
	location = models.CharField(max_length=250, null=True, blank=True)
	overview = models.TextField(null=True, blank=True)
	marital_status = models.CharField(max_length=100, null=True, blank=True)
	followers = models.ManyToManyField(User, related_name='followed_users')
	friends = models.ManyToManyField(User, related_name='+')

	@property
	def full_name(self):
		return f'{self.user.first_name} {self.user.last_name}'

	def get_profileimage(self):
		return self.profileimage_set.all()[0].profile_image.url

	def get_coverimage(self):
		return self.coverimage_set.all()[0].cover_image.url

class FriendRequest(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created',]

	def __str__(self):
		return f'{self.from_user.username} friend request to {self.to_user.username}'

class ProfileImage(models.Model):
	userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	profile_image = models.ImageField(upload_to='profile_images/%Y-%m-%d/', default='profile_images/placeholder.jpg')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)


class CoverImage(models.Model):
	userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	cover_image = models.ImageField(upload_to='cover_images/%Y-%m-%d/', default='cover_images/placeholder.jpg')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)
