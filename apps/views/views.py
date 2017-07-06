# Import django packages
from django.views import View
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _

# Import site apps
from apps.models import models
from apps.views import glossary as glossary_terms

class FrontView(View):
    """View of frontpage."""

    def get(self, request):
        offers  = models.Batch.objects.filter(category='of')[::3]
        demands = models.Batch.objects.filter(category='de')[::3]
        spaces  = models.Space.objects.filter(published=True)[::3]
        posts   = models.Post.objects.filter(published=True).order_by('-creation_date')[::4]
        return render(request, 'pages/front.html', locals())

class ResourcesView(View):
    """View of the resources section."""

    def get(self, request):
      resources = [
          {
              'url'  : reverse('legal-issues'),
              'icon' : 'icon-normativas',
              'label' : _('Aspectos legales'),
          },
          {
              'url'  : reverse('agreements'),
              'icon' : 'icon-acuerdos',
              'label' : _('Acuerdos'),
          },
          {
              'url'  : reverse('glossary'),
              'icon' : 'icon-glosario',
              'label' : _('Glosario'),
          },
          {
              'url'  : reverse('references'),
              'icon' : 'icon-link',
              'label' : _('Referencias'),
          },
      ]
      return render(request, 'pages/resources.html', locals())

class GlossaryView(View):
  """View of the site Glossary."""

  def get(self, request):
    glossary = glossary_terms.get()
    return render(request, 'pages/glossary.html', locals())

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

class AgreementsView(ListView):
    """View of the Agreement model instances."""

    model = models.Agreement

class BatchesView(ListView):
    """View of the Batches model instances."""

    model = models.Batch

    def get_queryset(self):
        queryset = models.Batch.objects.filter(quantity__gt=0)
        return queryset

class ReferencesView(ListView):
    """View of the Agreement model instances."""

    model = models.Reference

class ReusesView(ListView):
    """View of the Reuse model instances."""

    model = models.Space

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return models.Space.objects.filter(published=True, reuse=True).all().order_by('-active', '-creation_date')
        elif user.is_staff:
            return models.Space.objects.filter(reuse=True).order_by('-active', '-creation_date')
        published = models.Space.objects.filter(published=True, reuse=True)
        own       = models.Space.objects.filter(nodes__in=user.node_set)
        return (published | own).order_by('-active', '-creation_date')

class SpaceItemView(DetailView):
    """View of a Reuse model instance."""

    model = models.Space

    def get_context_data(self, **kwargs):
        context = super(SpaceItemView, self).get_context_data(**kwargs)
        obj     = super(SpaceItemView, self).get_object()
        context['blogposts'] = models.Post.objects.filter(space=obj)
        context['needs']     = models.Batch.objects.filter(category='de', space=obj)
        context['inventory'] = models.Batch.objects.filter(category='of', space=obj)
        return context
