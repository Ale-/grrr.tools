# Import django packages
from django.views import View
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _

# Import site apps
from apps.models import models


class FrontView(View):
    """View of frontpage."""

    def get(self, request):
        blog_posts = models.Post.objects.all().order_by('-creation_date')[::4]
        return render(request, 'pages/front.html', locals())

class ResourcesView(View):
    """View of the resources section."""

    def get(self, request):
      resources = [
          {
              'url'  : reverse('front'),
              'icon' : 'icon-normativas',
              'label' : _('Aspectos legales'),
          },
          {
              'url'  : reverse('front'),
              'icon' : 'icon-acuerdos',
              'label' : _('Acuerdos'),
          },
          {
              'url'  : reverse('front'),
              'icon' : 'icon-glosario',
              'label' : _('Glosario'),
          },
          {
              'url'  : reverse('front'),
              'icon' : 'icon-link',
              'label' : _('Referencias'),
          },
      ]
      return render(request, 'pages/resources.html', locals())

class BlogView(ListView):
    """View of the blog model instances."""

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = models.Post.objects.all().order_by('-creation_date')
        else:
            queryset = models.Post.objects.all().filter(published=True).order_by('-creation_date')
        return queryset

class BlogItemView(DetailView):
    """View of a blog model instance."""

    model = models.Post

class NodesView(ListView):
    """View of the blog model instances."""

    model = models.Node

class NodeItemView(DetailView):
    """View of a blog model instance."""

    model = models.Node
