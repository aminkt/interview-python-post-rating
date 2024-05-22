from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from posts.storage.models import PostModel, RatingModel

class ViewApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post = PostModel.objects.create(title='Test Post', content='This is a test post.')

    def test_view_posts(self):
        """
        Ensure we can view a list of posts.
        """
        url = reverse('post-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Post')

    def test_rate_post(self):
        """
        Ensure we can rate a post.
        """
        url = reverse('post-rate', args=[self.post.id])
        data = {'score': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating = RatingModel.objects.get(post=self.post, user=self.user)
        self.assertEqual(rating.score, 5)

        # Update the rating
        data = {'score': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating.refresh_from_db()
        self.assertEqual(rating.score, 3)