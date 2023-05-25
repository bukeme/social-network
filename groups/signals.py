from django.db.models.signals import post_save
from django.dispatch import receiver
from groups.models import CustomGroup, GroupProfileImage


@receiver(post_save, sender=CustomGroup)
def create_group_profile_image(sender, instance, created, *args, **kwargs):
    if created:
        GroupProfileImage.objects.create(group=instance)