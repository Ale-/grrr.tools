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
    url(r'^crea/post$', views.PostCreate.as_view(), name="create_post"),
    # Edit project form
    url(r'^edita/post/(?P<pk>.+)$', views.PostEdit.as_view(), name="edit_post"),
    # Remove project form
    url(r'^borra/post/(?P<pk>.+)$', views.PostDelete.as_view(), name="delete_post"),

    # Add material form
    url(r'^crea/material$', views.MaterialCreate.as_view(), name="create_material"),

]
