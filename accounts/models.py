from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save


def upload_location(instance, file_name):
    username = str(instance.user.username)
    return "%s/%s/%s" % (username, 'profile', file_name)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    profile_picture = models.ImageField(
            upload_to=upload_location,
            null=True,
            blank=True,
            height_field="height_field",
            width_field="width_field",
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


