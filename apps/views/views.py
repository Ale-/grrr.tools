# Import django packages
from django.views import View
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

# Import site apps
from apps.models import models
from apps.views import glossary as glossary_terms
from . import forms

class FrontView(View):
    """View of frontpage."""

    def get(self, request):
        offers  = models.Batch.objects.filter(category='of')[:4]
        demands = models.Batch.objects.filter(category='de')[:4]
        spaces  = models.Space.objects.filter(published=True)[:3]
        posts  = models.Post.objects.filter(published=True).order_by('-creation_date')[:3]
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

    def get_context_data(self, **kwargs):
        context = super(BlogItemView, self).get_context_data(**kwargs)
        obj     = super(BlogItemView, self).get_object()
        context['other_posts'] = models.Post.objects.filter(space=obj.space).exclude(pk=obj.pk)
        return context

class NodesView(ListView):
    """View of the blog model instances."""

    model = models.Node

    def get_queryset(self):
        queryset = models.Node.objects.all().order_by('name')
        return queryset

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

class BatchItemView(DetailView):
    """View of a Batch instance."""

    model = models.Batch

    def get_context_data(self, **kwargs):
        context = super(BatchItemView, self).get_context_data(**kwargs)
        obj     = super(BatchItemView, self).get_object()
        context['history'] = obj.milestones.order_by('date')
        return context


class TransferBatchView(View):
    """Form to transfer of a Batch instance."""

    title = _("Transfiere")
    form = forms.TransferBatchForm
    form__html_class = 'transfer'
    explanation = ('Al transferir materiales se actualiza de manera automática '
                  'el inventario del espacio que los recibe. Esta operación no se '
                  'puede modificar una vez realizada. Si hay algún error ponte en '
                  'contacto con el equipo GRRR')

    @method_decorator(login_required)
    def get(self, request, pk):
        batch = get_object_or_404(models.Batch, pk=pk)
        form = self.form()
        return render(request, 'pages/modelform-batches.html', {
            'form': form,
            'form__html_class' : self.form__html_class,
            'title' : self.title,
            'batch' : batch,
            'submit_text' : _('Transfiere'),
            'explanation' : _(self.explanation)
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        # Form
        form = self.form(request.POST)
        if form.is_valid():
            # Origin node
            batch = get_object_or_404(models.Batch, pk=pk)
            # Target node
            space = form.cleaned_data['space']
            # Create new batch in target node
            new_batch = models.Batch.objects.create(
                category     = 'of',
                space        = space,
                date         = form.cleaned_data['date'],
                material     = batch.material,
                image        = batch.image,
                quantity     = form.cleaned_data['quantity'],
                public_info  = batch.public_info,
                expiration   = None,
            )
            milestone = models.Milestone.objects.create(
                date     = form.cleaned_data['date'],
                space    = batch.space,
                category = 'TR',
                quantity = form.cleaned_data['quantity'],
            )
            new_batch.milestones.add(milestone)

            # Update current batch
            batch.quantity = batch.quantity - form.cleaned_data['quantity']
            if batch.quantity == 0:
                batch.delete()
                return HttpResponseRedirect(reverse('space', args=[space.slug]))
            batch.save(update_fields=('quantity',))
            return HttpResponseRedirect(reverse('batch', args=[batch.pk]))

        return render(request, 'pages/modelform-batches.html', {
            'form': form,
            'form__html_class' : self.form__html_class,
            'title' : self.title,
            'batch' : batch,
            'submit_text' : _('Transfiere'),
            'explanation' : _(self.explanation)
        })

class ActivateBatchView(View):
    """Form to transfer of a Batch instance."""

    title = _("Activa")
    form = forms.ActivateBatchForm
    form__html_class = 'activate'
    explanation = ('Al activa materiales se actualiza de manera automática '
                  'tu inventario y la cantidad de materiales activados por este espacio.'
                  'Esta operación no se puede modificar una vez realizada.'
                  'Si hay algún error ponte en contacto con el equipo GRRR')

    @method_decorator(login_required)
    def get(self, request, pk):
        batch = get_object_or_404(models.Batch, pk=pk)
        return render(request, 'pages/modelform-batches.html', {
            'form': self.form,
            'form__html_class' : self.form__html_class,
            'title' : self.title,
            'batch' : batch,
            'submit_text' : _('Activa'),
            'explanation' : _(self.explanation)
        })
