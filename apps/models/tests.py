from django.test import TestCase
from apps.models import models
from djgeojson.fields import PointField
from django.utils.text import slugify
from datetime import date

class NodeTest(TestCase):

    """ Create a node """
    def create_node(self):
        return models.Node.objects.create(
            name         = "Test node",
            description  = "Lorem ipsum",
            place        = "Test place",
            address      = "Test address",
            geom         = "POINT (0.0 0.0)",
            members      = 0
        )

    """ Test node creation """
    def test_node_creation(self):
        node = self.create_node()
        # Check string representation
        self.assertTrue(isinstance(node, models.Node))
        # Check fields
        self.assertTrue(node.__str__, node.name)
        self.assertEqual(node.slug, slugify(node.name))
        self.assertEqual(node.creation_date, date.today())
