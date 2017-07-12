from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from apps.models import models
from apps.users.models import UserProfile


class UserAccount(View):
    """Displays account of the current logged-in user."""

    @method_decorator(login_required)
    def get(self, request):
        # Dashboard data
        username       = request.user.username
        date_joined    = request.user.date_joined
        email          = request.user.email
        nodes          = models.Node.objects.filter(users__in=[request.user])
        spaces         = models.Space.objects.filter(nodes__in=nodes)
        received_sms   = models.Sms.objects.filter(receiver__in=spaces, replies__isnull=True).order_by('receiver', '-datetime')
        total_received = models.Sms.objects.filter(receiver__in=spaces).count()
        sent_sms       = models.Sms.objects.filter(emissor__in=spaces, replies__isnull=True)

        # Update User profile last_message_seen_date
        profile           = get_object_or_404(UserProfile, user=request.user)
        unseen_date       = profile.last_message_seen_datetime
        last_sms          = models.Sms.objects.order_by('-datetime').first()
        if not profile.last_message_seen_datetime or last_sms and last_sms.datetime > profile.last_message_seen_datetime:
            profile.last_message_seen_datetime = last_sms.datetime
            profile.save(update_fields=('last_message_seen_datetime',))

        return render(request, 'pages/dashboard.html', locals())
