import unittest
from unittest.mock import Mock

from posts.domain.exceptions import ValidationError
from posts.domain.use_cases import RatePostUseCase
from posts.storage.models import PostModel

class TestRatePostForm(unittest.TestCase):
    def setUp(self):
        # Create mocks for RatingRepositoryInterface and PostRepositoryInterface
        self.rating_repo_mock = Mock()
        self.post_repo_mock = Mock()
        self.form = RatePostUseCase(self.rating_repo_mock, self.post_repo_mock)

    def test_execute_correct(self):
        # Mock post and rating repositories
        post_id = 1
        user_id = 1
        score = 4
        self.post_repo_mock.get_post_by_id.return_value = Mock(id=post_id)

        # Execute the form
        self.form.execute(post_id, user_id, score)

        # Assert that the rate_post method was called with the correct arguments
        self.rating_repo_mock.rate_post.assert_called_once_with(post_id=post_id, user_id=user_id, score=score)

    def test_execute_incorrect_score(self):
        # Test incorrect score (not in range 0-5)
        post_id = 1
        user_id = 1
        score = 6  # Out of range
        with self.assertRaises(ValidationError):
            self.form.execute(post_id, user_id, score)

    def test_execute_post_not_exist(self):
        # Test post does not exist
        post_id = 1
        user_id = 1
        score = 4
        self.post_repo_mock.get_post_by_id.side_effect = PostModel.DoesNotExist

        with self.assertRaises(ValidationError):
            self.form.execute(post_id, user_id, score)