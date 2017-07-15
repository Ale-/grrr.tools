import json

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q

from apps.models import models


def nodes(request):
  """API endpoint to get all nodes in the site"""

  nodes = models.Node.objects.all()
  if len(nodes) > 0:
      jsondump = []
      for node in nodes:
          if(node.geom):
              item = {}
              item['lat']   =  node.geom['coordinates'][1]
              item['lon']   =  node.geom['coordinates'][0]
              item['popup'] =  "<h5>" + node.name + "</h5>" + \
                               "<p>" + node.description + "</p>"
              jsondump.append(item)
      return HttpResponse(json.dumps(jsondump, indent=4), content_type="application/json")
  else:
      return HttpResponse("If a tree falls in the woods and nobody is there to hear it, does it make a sound?")

def reuses(request):
  """API endpoint to get all reuses in the site"""

  nodes = models.Space.objects.filter(reuse=True, published=True)
  if len(nodes) > 0:
      jsondump = []
      for node in nodes:
          if(node.geom):
              item = {}
              item['lat']   =  node.geom['coordinates'][1]
              item['lon']   =  node.geom['coordinates'][0]
              item['popup'] =  "<img src='" + node.image.url + "' />" + \
                               "<h5><a href='" + reverse('space', args=[node.slug]) + "'>" + node.name + "</a></h5>" + \
                               "<p>" + node.summary + "</p>"
              jsondump.append(item)
      return HttpResponse(json.dumps(jsondump, indent=4), content_type="application/json")
  else:
      return HttpResponse("If a tree falls in the woods and nobody is there to hear it, does it make a sound?")

def batches(request):
  """API endpoint to get all batches in the site"""

  nodes = models.Batch.objects.filter( Q(category='of', quantity__gt=0) | Q(category='de'))
  if len(nodes) > 0:
      jsondump = []
      for node in nodes:
          if(node.space.geom):
              item = {}
              item['lat'] = node.space.geom['coordinates'][1]
              item['lon'] = node.space.geom['coordinates'][0]
              item['cat'] = node.category
              item['lnk'] = reverse('batch', args=[node.pk])
              item['nam'] = node.material.name
              item['mat'] = node.material.family
              item['des'] = node.public_info
              item['spa'] = node.space.name
              item['img'] = node.image.url if node.image else node.material.image.url
              jsondump.append(item)
      return HttpResponse(json.dumps(jsondump, indent=4), content_type="application/json")
  else:
      return HttpResponse("If a tree falls in the woods and nobody is there to hear it, does it make a sound?")
