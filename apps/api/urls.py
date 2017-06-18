from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  url(r'^nodos$', views.nodes, name="nodes_service"),
]
