from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View

from apps.models import models


class FrontView(View):
    """View of frontpage."""

    def get(self, request):
        blog_posts = models.Post.objects.all().order_by('-creation_date')[::4]
        return render(request, 'pages/front.html', locals())

class BlogView(ListView):
    """View of the blog model instances."""

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = models.Post.objects.all().order_by('-creation_date')
        else:
            queryset = models.Post.objects.all().filter(published=True).order_by('-creation_date')
        return queryset

class BlogItemView(DetailView):
    """View of a blog model instance."""

    model = models.Post

class NodesView(ListView):
    """View of the blog model instances."""

    model = models.Node

class NodeItemView(DetailView):
    """View of a blog model instance."""

    model = models.Post
