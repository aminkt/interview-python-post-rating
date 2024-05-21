from abc import ABC, abstractmethod

from posts.models import RatingModel


class RatingRepositoryInterface(ABC):
    @abstractmethod
    def get_user_rating_for_post(self, post_id: int, user_id: int) -> RatingModel:
        pass

    @abstractmethod
    def rate_post(self, post_id: int, user_id: int, score: int):
        pass