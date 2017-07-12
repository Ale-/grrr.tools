from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user                       = models.OneToOneField(User)
    last_message_seen_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """String representation of model instances."""
        return self.user.username

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.get_or_create(user=kwargs.get('instance'))
