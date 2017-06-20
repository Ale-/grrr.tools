# Import generic python packages
import json
# Import django packages
from django.test import Client
from django.test import TestCase
from django.urls import reverse
# Import contrib apps
from model_mommy import mommy
# Import site apps
from apps.models import models

class ViewsTest(TestCase):
    """ Test access to views """

    def test_front(self):
        """
        Checks front
        """
        c = Client()
        response = c.get(reverse('front'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        """
        Checks about
        """
        c = Client()
        response = c.get(reverse('about'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_resources(self):
        """
        Check resources section
        """
        c = Client()
        response = c.get(reverse('resources'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_legal_issues(self):
        """
        Check resources section
        """
        c = Client()
        response = c.get(reverse('legal-issues'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_agreements(self):
        """
        Check resources section
        """
        c = Client()
        response = c.get(reverse('agreements'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_glossary(self):
        """
        Check resources section
        """
        c = Client()
        response = c.get(reverse('glossary'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_references(self):
        """
        Check resources section
        """
        c = Client()
        response = c.get(reverse('references'))
        # Check empty view
        self.assertEqual(response.status_code, 200)

    def test_blog_view(self):
        """
        Checks Blog section
        """
        c = Client()
        response = c.get(reverse('blog'))
        # Check empty view
        self.assertEqual(response.status_code, 200)
        # Check prepopulated view
        self.test_post = mommy.make("models.Post", wysiwyg="Lorem ipsum.")
        response = c.get(reverse('blog'))
        content = response.context['object_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count(), 1)

    def test_blog_item_view(self):
        """
        Checks a single blogpost view
        """
        self.test_post = mommy.make("models.Post", wysiwyg="Lorem ipsum.")
        c = Client()
        response = c.get(reverse('blogpost', kwargs={'slug': self.test_post.slug}))
        # Check view
        self.assertEqual(response.status_code, 200)

    def test_nodes_view(self):
        """
        Checks front
        """
        c = Client()
        response = c.get(reverse('nodes'))
        # Check empty view
        self.assertEqual(response.status_code, 200)
        # Check prepopulated view
        self.test_post = mommy.make("models.Node")
        response = c.get(reverse('nodes'))
        content = response.context['object_list']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count(), 1)

    def test_node_item_view(self):
        """
        Checks a single node view
        """
        self.test_post = mommy.make("models.Node")
        c = Client()
        response = c.get(reverse('node', kwargs={'slug': self.test_post.slug}))
        # Check view
        self.assertEqual(response.status_code, 200)
