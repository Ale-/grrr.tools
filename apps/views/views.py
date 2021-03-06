# Import django packages
from django.views import View
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.db.models import Q

# Import site apps
from apps.models import models, categories
from apps.views import glossary as glossary_terms
from . import forms

class FrontView(View):
    """View of frontpage."""

    def get(self, request):
        batches   = models.Batch.objects.filter( Q(category='of', quantity__gt=0) | Q(category='de')).order_by('-date')[:6]
        spaces    = models.Space.objects.filter(published=True, reuse=True).order_by('-creation_date')[:3]
        posts     = models.Post.objects.filter(published=True).order_by('-creation_date')[:3]
        materials = categories.MATERIALS_BY_FAMILY
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
        queryset = models.Batch.objects.filter(Q(category='of', quantity__gt=0) | Q(category='de'))
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
            return models.Space.objects.filter(published=True).all().order_by('name', '-creation_date')
        elif user.is_staff:
            return models.Space.objects.all().order_by('name', '-creation_date')
        published = models.Space.objects.filter(published=True)
        own       = models.Space.objects.filter(nodes__in=user.users.all())
        return (published | own).order_by('name', '-creation_date')

class SpaceItemView(DetailView):
    """View of a Reuse model instance."""

    model = models.Space

    def get_context_data(self, **kwargs):
        context = super(SpaceItemView, self).get_context_data(**kwargs)
        obj     = super(SpaceItemView, self).get_object()
        context['blogposts'] = models.Post.objects.filter(space=obj)
        context['needs']     = models.Batch.objects.filter(category='de', space=obj)
        if obj.edit_permissions(self.request.user):
            context['inventory'] = models.Batch.objects.filter(category='of', space=obj)
        else:
            context['inventory'] = models.Batch.objects.filter(category='of', space=obj, quantity__gt=0)
        context['activated'] = models.Batch.objects.filter(category='ac', space=obj)
        context['recovered'] = models.Batch.objects.filter(category='re', space=obj)
        total_activated = 0
        for batch in context['activated']:
            if batch.quantity and batch.material.weight:
                total_activated += batch.quantity * batch.material.weight
        context['total_activated'] = total_activated/1000
        total_recovered = 0
        for batch in context['recovered']:
            total_recovered += (batch.quantity * batch.material.weight)
        context['total_recovered'] = total_recovered/1000
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
        form = self.form(pk=pk)
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
        # Origin node
        batch = get_object_or_404(models.Batch, pk=pk)
        # Form
        form = self.form(pk=pk, data=request.POST)
        if form.is_valid():
            # Target node
            space = form.cleaned_data['space']
            # Create new batch in target node
            target_batch = models.Batch.objects.create(
                category     = 'of',
                space        = space,
                date         = form.cleaned_data['date'],
                material     = batch.material,
                image        = batch.image,
                quantity     = 0,
                total        = form.cleaned_data['quantity'],
                public_info  = batch.public_info,
                expiration   = None,
            )

            # Create recovered batch in source node
            source_batch = models.Batch.objects.create(
                category     = 're',
                space        = batch.space,
                date         = form.cleaned_data['date'],
                material     = batch.material,
                image        = batch.image,
                quantity     = form.cleaned_data['quantity'],
                public_info  = batch.public_info,
                expiration   = None,
                target       = space
            )

            # Update milestones
            batch_milestones = batch.milestones.all()
            print(batch_milestones)
            if len(batch_milestones) > 0:
                target_batch.milestones.add( *[milestone.pk for milestone in batch_milestones] )
                source_batch.milestones.add( *[milestone.pk for milestone in batch_milestones] )

            milestone = models.Milestone.objects.create(date=form.cleaned_data['date'], space=batch.space)
            target_batch.milestones.add(milestone.pk)

            # Update current batch
            quantity = form.cleaned_data['quantity']
            batch.total -= quantity
            if quantity > batch.quantity:
                batch.quantity -= form.cleaned_data['quantity']
            batch.quantity = max(batch.quantity - quantity , 0)
            batch.save(update_fields=('quantity', 'total'))

            return HttpResponseRedirect(reverse('space', args=[batch.space.slug]))

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
            'form': self.form(pk=pk),
            'form__html_class' : self.form__html_class,
            'title' : self.title,
            'batch' : batch,
            'submit_text' : _('Activa'),
            'explanation' : _(self.explanation)
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        # Origin node
        batch = get_object_or_404(models.Batch, pk=pk)
        # Form
        form = self.form(pk=pk, data=request.POST)
        if form.is_valid():
            # Create new active
            new_batch = models.Batch.objects.create(
                category     = 'ac',
                space        = batch.space,
                date         = form.cleaned_data['date'],
                material     = batch.material,
                image        = batch.image,
                quantity     = form.cleaned_data['quantity'],
            )

            batch_milestones = batch.milestones.all()
            if len(batch_milestones) > 0:
                new_batch.milestones.add( *[milestone.pk for milestone in batch_milestones] )

            # Update current batch
            quantity = form.cleaned_data['quantity']
            batch.total -= quantity
            if quantity > batch.quantity:
                batch.quantity -= form.cleaned_data['quantity']
            batch.quantity = max(batch.quantity - quantity , 0)
            batch.save(update_fields=('quantity', 'total'))

            return HttpResponseRedirect(reverse('space', args=[batch.space.slug]))

        return render(request, 'pages/modelform-batches.html', {
            'form': form,
            'form__html_class' : self.form__html_class,
            'title' : self.title,
            'batch' : batch,
            'submit_text' : _('Activa'),
            'explanation' : _(self.explanation)
        })
