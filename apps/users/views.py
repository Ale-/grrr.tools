from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.models import models

class UserAccount(View):
    """Displays account of the current logged-in user."""

    @method_decorator(login_required)
    def get(self, request):
        username    = request.user.username
        date_joined = request.user.date_joined
        email       = request.user.email
        sms         = models.Sms.objects.all()
        nodes       = models.Node.objects.filter(users__in=[request.user])

        return render(request, 'pages/dashboard.html', locals())
