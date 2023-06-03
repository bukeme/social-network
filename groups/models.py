from django.db import models
from django.conf import settings
from django.urls import reverse


User = settings.AUTH_USER_MODEL

# Create your models here.

class CustomGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    about = models.TextField()
    members = models.ManyToManyField(User, related_name='group')
    admin_members = models.ManyToManyField(User, related_name='+')
    created = models.DateTimeField(auto_now_add=True)

    @property
    def members_count(self):
        return self.members.all().count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('home')
        return reverse('group_detail', args=[self.pk,])

    def get_profileimage(self):
        return self.groupprofileimage_set.first().image.url

    class Meta:
        ordering = ['-created']

class GroupProfileImage(models.Model):
    image = models.ImageField(upload_to='group_profile_images/%Y-%m-%d/', default='group_profile_images/placeholder.png')
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created',]
