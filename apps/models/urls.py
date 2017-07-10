from django.conf.urls import url

from . import views
from .forms import MaterialForm
from apps.utils.views import PopupFormView

urlpatterns = [
    # Add project form
    url(r'^crea/nodo$', views.NodeCreate.as_view(), name="create_node"),
    # Edit project form
    url(r'^edita/nodo/(?P<pk>.+)$', views.NodeEdit.as_view(), name="edit_node"),
    # Remove project form
    url(r'^borra/nodo/(?P<pk>.+)$', views.NodeDelete.as_view(), name="delete_node"),

    # Add project form
    url(r'^crea/espacio$', views.SpaceCreate.as_view(), name="create_space"),
    # Edit project form
    url(r'^edita/espacio/(?P<pk>.+)$', views.SpaceEdit.as_view(), name="edit_space"),
    # Remove project form
    url(r'^borra/espacio/(?P<pk>.+)$', views.SpaceDelete.as_view(), name="delete_space"),

    # Add project form
    url(r'^crea/post$', views.PostCreate.as_view(), name="create_post"),
    # Edit project form
    url(r'^edita/post/(?P<pk>.+)$', views.PostEdit.as_view(), name="edit_post"),
    # Remove project form
    url(r'^borra/post/(?P<pk>.+)$', views.PostDelete.as_view(), name="delete_post"),

    # Add batch form
    url(r'^crea/lote$', views.BatchCreate.as_view(), name="create_batch"),
    # Edit batch form
    url(r'^edita/lote/(?P<pk>.+)$', views.BatchEdit.as_view(), name="edit_batch"),
    # Remove batch form
    url(r'^borra/lote/(?P<pk>.+)$', views.BatchDelete.as_view(), name="delete_batch"),

    # Add material form
    url(r'^crea/material$', views.MaterialCreate.as_view(), name="create_material"),
    url(r'^anade/material$', PopupFormView.as_view(form_class=MaterialForm, template_name="pages/modelform-popup-material.html"), name="create_material_popup"),

    # Send SMS form
    url(r'^envia/sms$', views.SmsCreate.as_view(), name="create_sms"),
    # Send SMS to given space asking for given batch
    url(r'^envia/sms/a/(?P<slug>.+)/lote-(?P<pk>.+)$', views.SmsCreate.as_view(), name="batch_sms"),
    # Send SMS to given space form
    url(r'^envia/sms/a/(?P<slug>.+)$', views.SmsCreate.as_view(), name="send_sms_to"),
    # Reply SMS form
    url(r'^responde/sms/(?P<pk>.+)$', views.SmsReply.as_view(), name="reply_sms"),
]
