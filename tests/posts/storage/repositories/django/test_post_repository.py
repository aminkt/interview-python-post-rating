from django.test import TestCase
from unittest.mock import patch, MagicMock
from posts.storage.models import PostModel
from posts.storage.repositories.django.post_repository import DjangoPostRepository
from django.core.paginator import EmptyPage

class DjangoPostRepositoryTest(TestCase):
    def setUp(self):
        self.post_repo = DjangoPostRepository()

    @patch('posts.storage.models.PostModel.objects.all')
    @patch('posts.storage.models.RatingModel.objects.filter')
    @patch('django.core.paginator.Paginator.page')
    def test_get_paginated_posts(self, mock_page, mock_filter, mock_all):
        # Set up mock posts
        mock_post1 = MagicMock(spec=PostModel, id=1, title='Post 1', content='Content 1', created_at='2021-01-01', rate_count=10, score_sum=40)
        mock_post2 = MagicMock(spec=PostModel, id=2, title='Post 2', content='Content 2', created_at='2021-01-02', rate_count=20, score_sum=80)
        mock_all.return_value = [mock_post1, mock_post2]

        # Set up mock pagination
        mock_page.return_value.object_list = [mock_post1, mock_post2]

        # Set up mock user ratings
        mock_filter.return_value.values.return_value = [{'post_id': 1, 'score': 5}, {'post_id': 2, 'score': 4}]

        user_id = 1
        page = 1
        page_size = 10

        result = self.post_repo.get_paginated_posts(user_id, page, page_size)

        expected_result = [
            {
                'id': 1,
                'title': 'Post 1',
                'content': 'Content 1',
                'created_at': '2021-01-01',
                'rating_count': 10,
                'average_rating': 4.0,
                'user_score': 5,
            },
            {
                'id': 2,
                'title': 'Post 2',
                'content': 'Content 2',
                'created_at': '2021-01-02',
                'rating_count': 20,
                'average_rating': 4.0,
                'user_score': 4,
            },
        ]

        self.assertEqual(result, expected_result)
        mock_all.assert_called_once()
        mock_filter.assert_called_once_with(post_id__in=[1, 2], user_id=user_id)
        mock_page.assert_called_once_with(page)

    @patch('posts.storage.models.PostModel.objects.all')
    @patch('django.core.paginator.Paginator.page', side_effect=EmptyPage)
    def test_get_paginated_posts_empty_page(self, mock_page, mock_all):
        mock_all.return_value = []

        user_id = 1
        page = 1
        page_size = 10

        result = self.post_repo.get_paginated_posts(user_id, page, page_size)

        self.assertEqual(result, [])
        mock_all.assert_called_once()
        mock_page.assert_called_once_with(page)

    @patch('posts.storage.models.PostModel.objects.get')
    def test_get_post_by_id(self, mock_get):
        mock_post = MagicMock(spec=PostModel, id=1, title='Post 1', content='Content 1', created_at='2021-01-01')
        mock_get.return_value = mock_post

        post_id = 1
        result = self.post_repo.get_post_by_id(post_id)

        self.assertEqual(result, mock_post)
        mock_get.assert_called_once_with(id=post_id)
