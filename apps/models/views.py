from datetime import date

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.cache import never_cache
from django.forms import formset_factory, modelformset_factory
from django.utils.html import escape
from django.utils.decorators import method_decorator

from . import models, forms
from apps.utils.views import GenericCreate, GenericUpdate, GenericDelete

generic_template = 'pages/modelform.html'

#
# Node
#

node_explanation = ("Los nodos son los agentes miembros de la red del GRRR. "
                    "Un nodo puede ser una asociación, un colectivo, un proyecto "
                    "cultural o artístico, una institución... Las ofertas "
                    "y demandas de materiales se asocian a nuestros nodos.")


class NodeCreate(GenericCreate):
  """ Modelform view to create a Project object"""

  title = _('Añade un nodo')
  explanation = _(node_explanation)
  form_class = forms.NodeCreateForm
  dependencies = ['leaflet']
  model = models.Node
  template_name = generic_template
  form__html_class = 'node'


  def get_initial(self):
    super(NodeCreate, self).get_initial()
    return {
        'manager' : self.request.user
    }

  def form_valid(self, form):
    form.instance.manager = self.request.user
    return super(NodeCreate, self).form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(NodeCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Crea tu nodo')
    context['explanation'] = self.explanation
    return context

  def get_success_url(self):
    return reverse('node', args=(self.object.slug,))

class NodeEdit(GenericUpdate):
  """ Modelform view to edit a Project object"""

  title = _('Edita el nodo ')
  explanation = _(node_explanation)
  form_class = forms.NodeCreateForm
  dependencies = ['leaflet']
  model = models.Node
  template_name = generic_template
  form__html_class = 'node'

  def get_initial(self):
    super(NodeEdit, self).get_initial()
    return {
        'project_users' : self.object.users.all()
    }

  def get_success_url(self):
    return reverse('node', args=(self.object.slug,))

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    context['explanation'] = self.explanation
    context['form__html_class'] = 'node'
    context['submit_text'] = _('Edita este nodo')
    return context

class NodeDelete(GenericDelete):
  """ Modelform view to delete a Project object"""

  title = _('Borra un proyecto')
  model = models.Node

  def get_initial(self):
    super(NodeEdit, self).get_initial()
    if not self.object.edit_permissions( self.request.user ):
      raise PermissionDenied
    return self.initial

  def get_success_url(self):
    return reverse('nodes')

#
# Reuse
#

reuse_explanation = ("Los reusos cuentan cómo los nodos reutilizan los materiales. Pueden tener asociados los acuerdos "
                     "de cesión que se usaron (y se reflejaran en la sección 'Acuerdos' automáticamente) y lotes de materiales "
                     "que se contabilizarán como 'materiales activados' en las vistas de nodos. Intenta dar detalles que permitan "
                     "replicar las cualidades positivas de tu reuso y evitar los errores que tuviste.")

class ReuseCreate(GenericCreate):
  """ Modelform view to create a Reuse object"""

  title = _('Publica un reuso')
  explanation = _(reuse_explanation)
  form_class = forms.ReuseForm
  dependencies = ['leaflet']
  model = models.Reuse
  template_name = generic_template
  form__html_class = 'reuse'

  def get_context_data(self, **kwargs):
    context = super(ReuseCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Publica el reuso')
    context['explanation'] = self.explanation
    return context

  def get_success_url(self):
    return reverse('reuses')

class ReuseEdit(GenericUpdate):
  """ Modelform view to edit a Reuse object"""

  title = _('Editar')
  explanation = _(reuse_explanation)
  form_class = forms.ReuseForm
  dependencies = ['leaflet']
  model = models.Reuse
  template_name = generic_template

  def get_success_url(self):
    return reverse('reuse', args=(self.object.slug,))

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    context['explanation'] = self.explanation
    return context

class ReuseDelete(GenericDelete):
  """ Modelform view to delete a Reuse object"""

  title = _('Borra el reuso')
  model = models.Reuse

  def get_initial(self):
    super(ReuseDelete, self).get_initial()
    if not self.object.edit_permissions( self.request.user ):
      raise PermissionDenied
    return self.initial

  def get_context_data(self, **kwargs):
    context = super(GenericDelete, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    return context


  def get_success_url(self):
    return reverse('reuses')

#
# Material
#

material_explanation = ("Los materiales nos ayudan a tener una librería de datos homogénea "
                        "que nos sirva para documentar los lotes y hacer cálculos sobre las "
                        "transacciones de materiales.")

class MaterialCreate(GenericCreate):
  """ Modelform view to create a Project object"""

  title = _('Añade un material')
  explanation = _(material_explanation)
  form_class = forms.MaterialForm
  model = models.Material
  template_name = generic_template
  form__html_class = 'material'

  def get_context_data(self, **kwargs):
    context = super(MaterialCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Registra este material')
    context['explanation'] = self.explanation
    return context

  def get_success_url(self):
    #return reverse('node', args=(self.object.slug,))
    return reverse('materials')

#
# Post
#

post_explanation = "Los posts son los artículos que nutren el Blog de la plataforma."

class PostCreate(GenericCreate):
  """ Modelform view to create Blog posts"""

  title = _('Publica un post')
  form_class = forms.PostForm
  model = models.Post
  template_name = generic_template
  form__html_class = 'blogpost'

  def get_context_data(self, **kwargs):
    context = super(PostCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Publica este post')
    context['explanation'] = _(post_explanation)
    return context

  def get_success_url(self):
    return reverse('front')

class PostEdit(GenericUpdate):
  """ Modelform view to edit a Project object"""

  title = _('Edita el post')
  form_class = forms.PostForm
  model = models.Post
  template_name = generic_template
  form__html_class = 'blogpost'

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.title
    context['explanation'] = _(post_explanation)
    context['submit_text'] = _('Edita este post')
    return context

class PostDelete(GenericDelete):
  """ Modelform view to delete a Project object"""

  title = _('Borra este post')
  model = models.Post

  def get_success_url(self):
    return reverse('nodes')
