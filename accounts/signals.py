from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User 
from accounts.models import UserProfile

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, *args, **kwargs):
	if created:
		user_profile = UserProfile.objects.create(user=instance)
		user_profile.profileimage_set.create()
		user_profile.coverimage_set.create()
