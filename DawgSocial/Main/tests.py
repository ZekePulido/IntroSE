from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm

class LoginTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {'username': self.username,'password': self.password})
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'username': 'invalid_user','password':'invalid_password'})
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_authenticated)


class RegisterTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_valid_register(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        response = self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_register(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'differentpassword',
        }

        response = self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertFalse(User.objects.filter(username='testuser').exists())