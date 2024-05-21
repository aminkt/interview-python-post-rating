from posts.repositories.django.post_repository import DjangoPostRepository
from posts.repositories.django.rating_repository import DjangoRatingRepository
from posts.repositories.interfaces.post_repository_interface import PostRepositoryInterface
from posts.repositories.interfaces.rating_repository_interface import RatingRepositoryInterface


# Dependency container can be replaced whit smt more complicated but i want to keep it easy.
class Dependencies:
    @staticmethod
    def post_repository() -> PostRepositoryInterface:
        return DjangoPostRepository()

    @staticmethod
    def rating_repository() -> RatingRepositoryInterface:
        return DjangoRatingRepository()