from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserTest(TestCase):

    """ Test node creation """
    def test_user_creation(self):
        """
        Checks registration view and user registration
        """
        c = Client()
        register_response = c.post(reverse('registration_register'), data={
            'username':'test',
            'email':'test@example.com',
            'password1': 'the quick brown fox jumps over the lazy god',
            'password2': 'the quick brown fox jumps over the lazy god',
        }, follow=True)
        self.assertEqual(register_response.status_code, 200)
        user = User.objects.get(username='test')
        self.assertFalse(user)

        """
        Test login view
        """
        login_response = c.post(reverse('auth_login'), data={
            'username' : 'test',
            'password' : 'the quick brown fox jumps over the lazy god'
        }, follow=True)
        self.assertEqual(login_response.status_code, 200)
