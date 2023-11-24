from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm, PostForm, ShareForm
from .models import Post, Comment, Friend_Request, Profile


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

class PostInteractionTest(TestCase):
    def setUp(self):
        # Creating a user and a sample post
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(user=self.user, content='This is a sample post.')

    def test_like_post(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  

        self.assertTrue(self.post.liked_by.filter(id=self.user.id).exists())

    def test_comment_on_post(self):
        self.client.login(username=self.username, password=self.password)
        
        comment_text = 'Nice post!'
        response = self.client.post(reverse('post_comment', args=[self.post.id]), {'comment_text': comment_text})
        self.assertEqual(response.status_code, 302)  

        self.assertTrue(Comment.objects.filter(post=self.post, content=comment_text).exists())

    def test_repost_post(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse('share_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  

        self.assertTrue(Post.objects.filter(shared_user=self.user, content=self.post.content).exists())

class FriendRequestTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)

        self.friend_request = Friend_Request.objects.create(from_user=self.user1, to_user=self.user2)

    def test_send_friend_request(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('send_friend_request', kwargs={'user_id': self.user2.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Friend_Request.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    def test_accept_friend_request(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('accept_friend_request', kwargs={'requestID': self.friend_request.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Friend_Request.objects.filter(id=self.friend_request.id).exists())
        self.assertTrue(self.user2.profile.friends.filter(id=self.user1.id).exists())

    def test_reject_friend_request(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(reverse('reject_friend_request', kwargs={'requestID': self.friend_request.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Friend_Request.objects.filter(id=self.friend_request.id).exists())

    def test_withdraw_friend_request(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('withdraw_friend_request', kwargs={'requestID': self.friend_request.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Friend_Request.objects.filter(id=self.friend_request.id).exists())

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

