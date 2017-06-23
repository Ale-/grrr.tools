import json

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from model_mommy import mommy

from apps.models import models


class ApiTest(TestCase):
    """ Test Api endpoints """

    def test_nodes_endpoint(self):
        """
        Checks registration view and user registration
        """
        c = Client()
        nodes_response = c.get(reverse('api:nodes_service'))
        # Check empty view
        self.assertEqual(nodes_response.status_code, 200)
        self.assertEqual(nodes_response.content.decode("utf-8"), "If a tree falls in the woods and nobody is there to hear it, does it make a sound?")
        # Check view with contents
        test_post = mommy.make("models.Node", geom=json.loads('{ "type": "Point", "coordinates": [ 0 , 0 ] }'))
        nodes_response = c.get(reverse('api:nodes_service'))
        content = nodes_response.json()
        self.assertEqual(nodes_response.status_code, 200)
        self.assertEqual(len(content), 1)

    def test_reuses_endpoint(self):
        """
        Checks registration view and user registration
        """
        c = Client()
        reuses_response = c.get(reverse('api:reuses_service'))
        # Check empty view
        self.assertEqual(reuses_response.status_code, 200)
        self.assertEqual(reuses_response.content.decode("utf-8"), "If a tree falls in the woods and nobody is there to hear it, does it make a sound?")
        # Check view with contents
        test_post = mommy.make("models.Reuse", wysiwyg="Lorem ipsum.", geom=json.loads('{ "type": "Point", "coordinates": [ 0 , 0 ] }'))
        reuses_response = c.get(reverse('api:reuses_service'))
        content = reuses_response.json()
        self.assertEqual(reuses_response.status_code, 200)
        self.assertEqual(len(content), 1)
