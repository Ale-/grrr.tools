# Import generic python packages
from datetime import date
# Import django packages
from django.test import TestCase
from django.utils.text import slugify
# Import contrib apps
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
from djgeojson.fields import PointField
# Import site apps
from apps.models import models

class NodeTest(TestCase):
    """ Test Nodes creation """

    def test_node_creation(self):
        node = mommy.make("models.Node")
        # Check string representation
        self.assertTrue(isinstance(node, models.Node))
        # Check fields
        self.assertEqual(node.__str__(), node.name)
        self.assertEqual(node.slug, slugify(node.name))
        self.assertEqual(node.creation_date, date.today())

class ReuseTest(TestCase):
    """ Test Reuses creation """

    def test_reuse_creation(self):
        node = mommy.make("models.Reuse", wysiwyg="Lorem ipsum.")
        # Check string representation
        self.assertTrue(isinstance(node, models.Reuse))
        # Check fields
        self.assertEqual(node.__str__(), node.name)
        self.assertEqual(node.slug, slugify(node.name))

class MaterialTest(TestCase):
    """ Test Materials creation """

    def test_node_creation(self):
        node = mommy.make("models.Material")
        # Check string representation
        self.assertTrue(isinstance(node, models.Material))
        # Check fields
        self.assertEqual(node.__str__(), node.name)
        self.assertEqual(node.slug, slugify(node.name))
        self.assertEqual(node.creation_date, date.today())

class PostTest(TestCase):
    """ Test Posts creation """

    def test_post_creation(self):
        post = mommy.make("models.Post", wysiwyg="Lorem ipsum.")
        # Check string representation
        self.assertTrue(isinstance(post, models.Post))
        # Check fields
        self.assertEqual(post.__str__(), post.title)
        self.assertEqual(post.slug, slugify(post.title))
        self.assertEqual(post.creation_date, date.today())

class AgreementTest(TestCase):
    """ Test Agreements creation """

    def test_post_creation(self):
        post = mommy.make("models.Agreement")
        # Check string representation
        self.assertTrue(isinstance(post, models.Agreement))
        # Check fields
        self.assertEqual(post.__str__(), post.title)


class ReferenceTest(TestCase):
    """ Test References creation """

    def test_post_creation(self):
        post = mommy.make("models.Reference")
        # Check string representation
        self.assertTrue(isinstance(post, models.Reference))
        # Check fields
        self.assertEqual(post.__str__(), post.name)

class SmsTest(TestCase):
    """ Test Sms creation """

    def test_sms_creation(self):
        emissor = mommy.make('models.Node')
        receiver = mommy.make('models.Node')
        sms = mommy.make('models.Sms', emissor=emissor, receiver=receiver)
        # Check string representation
        self.assertTrue(isinstance(sms, models.Sms))
        # Check fields
        self.assertEqual(sms.__str__(), "Mensaje de " + sms.emissor.name + " a " + sms.receiver.name + " del " + str(sms.date))
