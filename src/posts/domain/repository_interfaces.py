from abc import ABC, abstractmethod
from typing import List, Dict, Any

from posts.storage.models import RatingModel, PostModel


class PostRepositoryInterface(ABC):
    @abstractmethod
    def get_paginated_posts(self, user_id: int, page: int, page_size: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_post_by_id(self, id: int) -> PostModel:
        pass

class RatingRepositoryInterface(ABC):
    @abstractmethod
    def get_user_rating_for_post(self, post_id: int, user_id: int) -> RatingModel:
        pass

    @abstractmethod
    def rate_post(self, post_id: int, user_id: int, score: int):
        pass

    @abstractmethod
    def queue_rate_for_delayed_effect(self, post_id: int, user_id: int, score: int):
        pass

    @abstractmethod
    def get_queued_rate_ids(self, page: int) -> List[int]:
        pass

    @abstractmethod
    def apply_pending_rates(self, rate_ids: List[int]):
        pass