from abc import ABC, abstractmethod
from typing import List, Dict, Any

from posts.models import PostModel


class PostRepositoryInterface(ABC):
    @abstractmethod
    def get_paginated_posts(self, user_id: int, page: int, page_size: int = 10) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_post_by_id(self, id: int) -> PostModel:
        pass