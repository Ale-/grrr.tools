from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'api'

urlpatterns = [
  url(r'^nodos$', views.nodes, name="nodes_service"),
  url(r'^reusos$', views.reuses, name="reuses_service"),
  url(r'^batches$', views.batches, name="batches_service"),
]
