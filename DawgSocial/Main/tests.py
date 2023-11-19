from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': self.username,'password': self.password})
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'username': 'invalid_user','password':'invalid_password'})
        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    