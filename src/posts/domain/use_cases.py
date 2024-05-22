import threading
from abc import ABC, abstractmethod

from posts.domain.exceptions import ValidationError
from posts.domain.repository_interfaces import RatingRepositoryInterface, PostRepositoryInterface
from posts.storage.models import PostModel

class BaseUseCase(ABC):
    @abstractmethod
    def execute(self):
        pass

class RatePostUseCase:
    def __init__(self, rating_repo: RatingRepositoryInterface, post_repo: PostRepositoryInterface):
        self.__rating_repo = rating_repo
        self.__post_repo = post_repo

    def execute(self, post_id: int, user_id: int, score: int):
        if score not in range (0, 6):
            raise ValidationError('Score must be between 0 and 5')

        try:
            post = self.__post_repo.get_post_by_id(post_id)
            if post.rate_count < 50:
                # For post which have not any rate, till 50 rates we will apply them on the post rate.
                self.__rating_repo.rate_post(post_id=post.id, user_id=user_id, score=score)
            else:
                # If post has more than 50 rates, we will queue new ratings to apply them later
                self.__rating_repo.queue_rate_for_delayed_effect(post_id=post.id, user_id=user_id, score=score)

        except PostModel.DoesNotExist:
            raise ValidationError('Post does not exist')