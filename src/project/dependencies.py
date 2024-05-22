from posts.domain.repository_interfaces import PostRepositoryInterface, RatingRepositoryInterface
from posts.storage.repositories.django.post_repository import DjangoPostRepository
from posts.storage.repositories.django.rating_repository import DjangoRatingRepository


# Dependency container can be replaced whit smt more complicated but i want to keep it easy.
class Dependencies:
    @staticmethod
    def post_repository() -> PostRepositoryInterface:
        return DjangoPostRepository()

    @staticmethod
    def rating_repository() -> RatingRepositoryInterface:
        return DjangoRatingRepository()