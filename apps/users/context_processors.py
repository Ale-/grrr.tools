from apps.models import models
from django.shortcuts import get_object_or_404
from apps.users.models import UserProfile

def unseen_messages(request):
    """Injects into global context number of user's unseen messages"""

    nodes            = models.Node.objects.filter(users__in=[request.user])
    spaces           = models.Space.objects.filter(nodes__in=nodes)
    profile_datetime = get_object_or_404(UserProfile, user=request.user).last_message_seen_datetime
    sms              = models.Sms.objects.filter(receiver__in=spaces, datetime__gt=profile_datetime).count()

    return { 'sms' : sms }
