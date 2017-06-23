from django.conf.urls import url
from . import views


urlpatterns = [
    # Add project form
    url(r'^crea/nodo$', views.NodeCreate.as_view(), name="create_node"),
    # Edit project form
    url(r'^edita/nodo/(?P<pk>.+)$', views.NodeEdit.as_view(), name="edit_node"),
    # Remove project form
    url(r'^borra/nodo/(?P<pk>.+)$', views.NodeDelete.as_view(), name="delete_node"),

    # Add project form
    url(r'^crea/reuso$', views.ReuseCreate.as_view(), name="create_reuse"),
    # Edit project form
    url(r'^edita/reuso/(?P<pk>.+)$', views.ReuseEdit.as_view(), name="edit_reuse"),
    # Remove project form
    url(r'^borra/reuso/(?P<pk>.+)$', views.ReuseDelete.as_view(), name="delete_reuse"),

    # Add project form
    url(r'^crea/post$', views.PostCreate.as_view(), name="create_post"),
    # Edit project form
    url(r'^edita/post/(?P<pk>.+)$', views.PostEdit.as_view(), name="edit_post"),
    # Remove project form
    url(r'^borra/post/(?P<pk>.+)$', views.PostDelete.as_view(), name="delete_post"),

    # Add material form
    url(r'^crea/material$', views.MaterialCreate.as_view(), name="create_material"),

    # Add SMS form
    url(r'^envia/sms$', views.SmsCreate.as_view(), name="create_sms"),
    # Add SMS form
    url(r'^envia/sms/a/(?P<slug>.+)$$', views.SmsCreate.as_view(), name="send_sms_to"),
]
