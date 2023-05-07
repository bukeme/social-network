from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	other_name = models.CharField(max_length=200, null=True, blank=True)
	birthday = models.DateField(null=True, blank=True)
	phone = models.CharField(max_length=50, null=True, blank=True)
	occupation = models.CharField(max_length=200, null=True, blank=True)
	location = models.CharField(max_length=250, null=True, blank=True)
	overview = models.TextField(null=True, blank=True)
	marital_status = models.CharField(max_length=100, null=True, blank=True)

	def get_profileimage(self):
		return self.profileimage_set.all()[0].image.url

	def get_coverimage(self):
		return self.coverimage_set.all()[0].image.url

class ProfileImage(models.Model):
	userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='profile_images/%Y-%m-%d/', default='profile_images/placeholder.jpg')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)


class CoverImage(models.Model):
	userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='cover_images/%Y-%m-%d/', default='cover_images/placeholder.jpg')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)
