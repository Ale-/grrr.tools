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
# Project Views
#

node_explanation = ("Los nodos son los agentes miembros de la red del GRRR. "
                       "Un nodo puede ser una asociación, un colectivo, un proyecto"
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

  def get_context_data(self, **kwargs):
    context = super(NodeCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Crea tu nodo')
    return context

  def get_success_url(self):
    return reverse('node', args=(self.object.slug,))


class NodeEdit(GenericUpdate):
  """ Modelform view to edit a Project object"""

  title = _('Editar')
  explanation = _(node_explanation)
  form_class = forms.NodeUpdateForm
  dependencies = ['leaflet']
  model = models.Node
  template_name = generic_template

  def get_initial(self):
    super(ProjectEdit, self).get_initial()
    return {
        'project_users' : self.object.users.all()
    }

  def get_success_url(self):
    return reverse('node', args=(self.object.slug,))

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
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
