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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from . import models, forms
from apps.utils.views import GenericCreate, GenericUpdate, GenericDelete

generic_template = 'pages/modelform.html'
delete_template  = 'pages/modelform--delete.html'

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
    return reverse('nodes')

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
    return reverse('nodes')

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    context['explanation'] = self.explanation
    context['form__html_class'] = 'node'
    context['delete_button_arg'] = self.object.id
    context['submit_text'] = _('Edita este nodo')
    return context

class NodeDelete(GenericDelete):
  """ Modelform view to delete a Project object"""

  title = _('Borra el nodo')
  template_name = delete_template
  model = models.Node

  def get_context_data(self, **kwargs):
    context = super(GenericDelete, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    context['form__html_class'] = 'node'
    context['submit_text'] = _('Borrar este contenido')
    return context

  def get_initial(self):
    super(NodeEdit, self).get_initial()
    if not self.object.edit_permissions( self.request.user ):
      raise PermissionDenied
    return self.initial

  def get_success_url(self):
    return reverse('nodes')

#
# Space
#

space_explanation = ("Los espacios son lo que su nombre indica: espacios reales que forman parte de la red GRRR. Por ejemplo "
                     "podrían ser espacios: el almacén municipal de un ayuntamiento, el taller de un nodo o un solar dónde se "
                     "está creando un huerto comunitario a partir de materiales reutilizados. Los materiales se mueven entre "
                     "espacios y son los espacios los que tienen asociadas ofertas y demandas. Los espacios también pueden tener "
                     "asociados documentos de cesión y disponen de una bitácora en la plataforma. ")

class SpaceCreate(GenericCreate):
  """ Modelform view to create a Space object"""

  title = _('Añade un espacio a la red GRRR')
  explanation = _(space_explanation)
  form_class = forms.SpaceForm
  dependencies = ['leaflet']
  model = models.Space
  template_name = generic_template
  form__html_class = 'space'

  def get_context_data(self, **kwargs):
    context = super(SpaceCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Crea este contenido')
    context['explanation'] = self.explanation
    return context

  def get_success_url(self):
    return reverse('space', args=(self.object.slug,))

class SpaceEdit(GenericUpdate):
  """ Modelform view to edit a Space object"""

  title = _('Edita')
  explanation = _(space_explanation)
  form_class = forms.SpaceForm
  dependencies = ['leaflet']
  model = models.Space
  template_name = generic_template

  def get_success_url(self):
    return reverse('space', args=(self.object.slug,))

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    context['explanation'] = self.explanation
    context['form__html_class'] = 'space'
    context['submit_text'] = _('Guardar los cambios')
    context['delete_button_arg'] = self.object.id
    return context

class SpaceDelete(GenericDelete):
  """ Modelform view to delete a Space object"""

  title = _('Borra el reuso')
  model = models.Space
  template_name = delete_template

  def get_initial(self):
    super(SpaceDelete, self).get_initial()
    if not self.object.edit_permissions( self.request.user ):
      raise PermissionDenied
    return self.initial

  def get_context_data(self, **kwargs):
    context = super(GenericDelete, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.name
    context['form__html_class'] = 'space'
    context['submit_text'] = _('Borra este contenido')
    return context


  def get_success_url(self):
    return reverse('dashboard')

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

post_explanation = ("Los posts son los artículos que nutren el Blog de la plataforma. "
                    "Todos los espacios tienen un blog asociado en el que pueden publicar "
                    "sus logros, fallos, convocatorias, etc.")

class PostCreate(GenericCreate):
  """ Modelform view to create Blog posts"""

  title = _('Publica un post')
  form_class = forms.PostForm
  model = models.Post
  template_name = generic_template
  form__html_class = 'post'

  def get_initial(self):
    super(PostCreate, self).get_initial()
    return {
        'user' : self.request.user
    }

  def get_context_data(self, **kwargs):
    context = super(PostCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Publica este post')
    context['explanation'] = _(post_explanation)
    return context

  def get_success_url(self):
    return reverse('blogpost', args=(self.object.slug,))

class PostEdit(GenericUpdate):
  """ Modelform view to edit a Project object"""

  title = _('Edita el post')
  form_class = forms.PostForm
  model = models.Post
  template_name = generic_template
  form__html_class = 'post'

  def get_initial(self):
    super(PostEdit, self).get_initial()
    return {
        'user' : self.request.user
    }

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.title
    context['explanation'] = _(post_explanation)
    context['submit_text'] = _('Edita este post')
    context['form__html_class'] = 'post'
    context['delete_button_arg'] = self.object.id
    return context

  def get_success_url(self):
    return reverse('blogpost', args=(self.object.slug,))


class PostDelete(GenericDelete):
  """ Modelform view to delete a Project object"""

  title = _('Borra el post')
  model = models.Post
  template_name = delete_template

  def get_success_url(self):
     if self.object.space:
         return reverse('space', args=(self.object.space.slug,))
     return reverse('blog')

  def get_context_data(self, **kwargs):
    context = super(GenericDelete, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.title
    context['explanation'] = _(post_explanation)
    context['submit_text'] = _('Borrar')
    context['form__html_class'] = 'post'
    return context


#
# Mensaje
#

sms_explanation = ("Los mensajes son el canal de comunicación entre los espacios de la red."
                   "Los mensajes son visibles por los usuarios de los colectivos que trabajan en "
                   "dichos espacios. Puedes ver tus mensajes en tu perfil de usuari@")

class SmsCreate(GenericCreate):
  """ Modelform view to create a Sms object"""

  title = _('Envía un mensaje')
  explanation = _(sms_explanation)
  form_class = forms.SmsForm
  model = models.Sms
  template_name = generic_template
  form__html_class = 'sms'

  def get_initial(self):
    super(SmsCreate, self).get_initial()
    context = { 'user' : self.request.user }
    if 'slug' in self.kwargs:
        context['receiver'] = get_object_or_404(models.Space, slug=self.kwargs['slug'])
    if 'pk' in self.kwargs:
        context['batch'] = get_object_or_404(models.Batch, pk=self.kwargs['pk'])
    return context

  def form_valid(self, form):
    form.instance.author = self.request.user
    form.instance.date   = date.today()
    return super(SmsCreate, self).form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(SmsCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Envía el mensaje')
    context['explanation'] = self.explanation
    return context

  def get_success_url(self):
    return reverse('dashboard')

class SmsReply(GenericCreate):
  """ Modelform view to create a Sms object"""

  title = _('Responde a un mensaje')
  explanation = _(sms_explanation)
  form_class = forms.SmsForm
  model = models.Sms
  template_name = 'pages/modelform-sms-reply.html'
  form__html_class = 'sms'

  def get_initial(self):
    super(SmsReply, self).get_initial()
    replied = models.Sms.objects.filter(pk=self.kwargs['pk']).first()
    return {
        'user'     : self.request.user,
        'emissor'  : replied.receiver,
        'receiver' : replied.emissor,
        'batch'    : replied.batch if replied.batch else None
    }

  def form_valid(self, form):
    form.instance.author  = self.request.user
    form.instance.date    = date.today()
    replied = models.Sms.objects.filter(pk=self.kwargs['pk']).first()
    form.instance.replies = replied
    return super(SmsReply, self).form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(SmsReply, self).get_context_data(**kwargs)
    replied = models.Sms.objects.filter(pk=self.kwargs['pk']).first()
    context['submit_text'] = _('Envía el mensaje')
    context['explanation'] = self.explanation
    context['replied'] = replied
    return context

  def get_success_url(self):
    return reverse('dashboard')

#
# Mensaje
#

batch_explanation = ("Los lotes son partidas de un mismo material y asociadas a un espacio.")

class BatchCreate(GenericCreate):
  """ Modelform view to create a Batch object"""

  title = _('Añade un lote')
  explanation = _(batch_explanation)
  form_class = forms.BatchForm
  model = models.Batch
  template_name = generic_template
  form__html_class = 'batch'

  def get_initial(self):
    super(BatchCreate, self).get_initial()
    context = { 'user' : self.request.user }
    return context

  def get_context_data(self, **kwargs):
    context = super(BatchCreate, self).get_context_data(**kwargs)
    context['submit_text'] = _('Registra este lote')
    context['explanation'] = self.explanation
    return context

  def get_success_url(self):
    return reverse('batch', args=(self.object.pk,))


class BatchEdit(GenericUpdate):
  """ Modelform view to edit a Batch object"""

  title = _('Edita este lote')
  explanation = _(batch_explanation)
  form_class = forms.BatchForm
  dependencies = ['leaflet']
  model = models.Batch
  template_name = generic_template
  form__html_class = 'batch'

  def get_initial(self):
    super(BatchEdit, self).get_initial()
    context = { 'user' : self.request.user }
    return context

  def get_success_url(self):
    return reverse('batch', args=(self.object.pk,))

  def get_context_data(self, **kwargs):
    context = super(GenericUpdate, self).get_context_data(**kwargs)
    context['explanation'] = self.explanation
    context['form__html_class'] = 'batch'
    context['title'] = self.title
    context['submit_text'] = _('Guarda los cambios')
    context['delete_button_arg'] = self.object.id
    return context


class BatchDelete(GenericDelete):
  """ Modelform view to delete a Batch object"""

  title = _('Borra el lote')
  model = models.Batch
  template_name = delete_template

  def get_context_data(self, **kwargs):
    context = super(GenericDelete, self).get_context_data(**kwargs)
    context['title'] = self.title + (' ') + self.object.batch_id()
    context['form__html_class'] = 'batch'
    context['submit_text'] = _('Borrar este contenido')
    return context

  def get_initial(self):
    super(NodeEdit, self).get_initial()
    if not self.object.edit_permissions( self.request.user ):
      raise PermissionDenied
    return self.initial

  def get_success_url(self):
    return reverse('reuses')


class PopupMaterialFormView(LoginRequiredMixin, FormView):
    """Popup to create Material objects."""

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script type="text/javascript">opener.dismissAddRelatedObjectPopup(window, "%s", "%s");</script>' % (\
                            escape(instance.id),
                            escape(instance.name)
        ))

class PopupAgreementFormView(LoginRequiredMixin, FormView):
    """Popup to create Agreement objects."""

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script type="text/javascript">opener.dismissAddRelatedObjectPopup(window, "%s", "%s");</script>' % (\
                            escape(instance.id),
                            escape(instance.title)
        ))
