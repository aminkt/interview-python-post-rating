import unittest
from unittest.mock import MagicMock, patch
from posts.domain.exceptions import ValidationError
from posts.domain.repository_interfaces import RatingRepositoryInterface, PostRepositoryInterface
from posts.storage.models import PostModel
from posts.domain.use_cases import RatePostUseCase

class RatePostUseCaseTest(unittest.TestCase):
    def setUp(self):
        self.rating_repo = MagicMock(spec=RatingRepositoryInterface)
        self.post_repo = MagicMock(spec=PostRepositoryInterface)
        self.use_case = RatePostUseCase(rating_repo=self.rating_repo, post_repo=self.post_repo)

    def test_score_validation_error(self):
        with self.assertRaises(ValidationError):
            self.use_case.execute(post_id=1, user_id=1, score=6)
        with self.assertRaises(ValidationError):
            self.use_case.execute(post_id=1, user_id=1, score=-1)

    def test_rate_post_directly(self):
        post = MagicMock(spec=PostModel)
        post.rate_count = 49
        self.post_repo.get_post_by_id.return_value = post

        self.use_case.execute(post_id=1, user_id=1, score=3)

        self.rating_repo.rate_post.assert_called_once_with(post_id=post.id, user_id=1, score=3)
        self.rating_repo.queue_rate_for_delayed_effect.assert_not_called()

    def test_queue_rate_for_delayed_effect(self):
        post = MagicMock(spec=PostModel)
        post.rate_count = 50
        self.post_repo.get_post_by_id.return_value = post

        self.use_case.execute(post_id=1, user_id=1, score=3)

        self.rating_repo.queue_rate_for_delayed_effect.assert_called_once_with(post_id=post.id, user_id=1, score=3)
        self.rating_repo.rate_post.assert_not_called()

    def test_post_does_not_exist(self):
        self.post_repo.get_post_by_id.side_effect = PostModel.DoesNotExist

        with self.assertRaises(ValidationError):
            self.use_case.execute(post_id=1, user_id=1, score=3)

