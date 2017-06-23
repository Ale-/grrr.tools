import json

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse

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
              item['popup'] =  "<h5><a href='" + reverse('node', args=[node.slug]) + "'>" + node.name + "</a></h5>" + \
                                   "<p>" + node.description + "</p>"
              jsondump.append(item)
      return HttpResponse(json.dumps(jsondump, indent=4), content_type="application/json")
  else:
      return HttpResponse("If a tree falls in the woods and nobody is there to hear it, does it make a sound?")

def reuses(request):
  """API endpoint to get all reuses in the site"""

  nodes = models.Reuse.objects.all()
  if len(nodes) > 0:
      jsondump = []
      for node in nodes:
          if(node.geom):
              item = {}
              item['lat']   =  node.geom['coordinates'][1]
              item['lon']   =  node.geom['coordinates'][0]
              item['popup'] =  "<h5><a href='" + reverse('node', args=[node.slug]) + "'>" + node.name + "</a></h5>" + \
                                   "<p>" + node.summary + "</p>"
              jsondump.append(item)
      return HttpResponse(json.dumps(jsondump, indent=4), content_type="application/json")
  else:
      return HttpResponse("If a tree falls in the woods and nobody is there to hear it, does it make a sound?")
