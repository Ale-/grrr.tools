# Import generic python packages
from datetime import date
# Import django packages
from django.test import TestCase
from django.utils.text import slugify
# Import contrib apps
from model_mommy import mommy
from djgeojson.fields import PointField
# Import site apps
from apps.models import models

class NodeTest(TestCase):
    """ Test node creation """

    def test_node_creation(self):
        node = mommy.make("models.Node")
        # Check string representation
        self.assertTrue(isinstance(node, models.Node))
        # Check fields
        self.assertTrue(node.__str__, node.name)
        self.assertEqual(node.slug, slugify(node.name))
        self.assertEqual(node.creation_date, date.today())

class MaterialTest(TestCase):
    """ Test material creation """

    def test_node_creation(self):
        node = mommy.make("models.Material")
        # Check string representation
        self.assertTrue(isinstance(node, models.Material))
        # Check fields
        self.assertTrue(node.__str__, node.name)
        self.assertEqual(node.slug, slugify(node.name))
        self.assertEqual(node.creation_date, date.today())

class PostTest(TestCase):
    """ Test node creation """

    def test_post_creation(self):
        post = mommy.make("models.Post", wysiwyg="Lorem ipsum.")
        # Check string representation
        self.assertTrue(isinstance(post, models.Post))
        # Check fields
        self.assertTrue(post.__str__, post.title)
        self.assertEqual(post.slug, slugify(post.title))
        self.assertEqual(post.creation_date, date.today())

class AgreementTest(TestCase):
    """ Test node creation """

    def test_post_creation(self):
        post = mommy.make("models.Agreement")
        # Check string representation
        self.assertTrue(isinstance(post, models.Agreement))
        # Check fields
        self.assertTrue(post.__str__, post.title)


class ReferenceTest(TestCase):
    """ Test node creation """

    def test_post_creation(self):
        post = mommy.make("models.Reference")
        # Check string representation
        self.assertTrue(isinstance(post, models.Reference))
        # Check fields
        self.assertTrue(post.__str__, post.name)
