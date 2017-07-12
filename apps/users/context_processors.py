from apps.models import models
from django.shortcuts import get_object_or_404
from apps.users.models import UserProfile

def unseen_messages(request):
    """Injects into global context number of user's unseen messages"""

    if request.user.is_authenticated:
        nodes            = models.Node.objects.filter(users__in=[request.user])
        spaces           = models.Space.objects.filter(nodes__in=nodes)
        #profile_datetime = get_object_or_404(UserProfile, user=request.user).last_message_seen_datetime
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if profile.last_message_seen_datetime:
            sms = models.Sms.objects.filter(receiver__in=spaces, datetime__gt=profile.last_message_seen_datetime).count()
        else:
            sms = models.Sms.objects.filter(receiver__in=spaces).count()
        return { 'sms' : sms }

    return { 'sms' : 0 }
