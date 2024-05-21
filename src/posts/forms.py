from posts.exceptions import ValidationError
from posts.models import PostModel
from posts.repositories.interfaces.post_repository_interface import PostRepositoryInterface
from posts.repositories.interfaces.rating_repository_interface import RatingRepositoryInterface


class RatePostForm:
    def __init__(self, rating_repo: RatingRepositoryInterface, post_repo: PostRepositoryInterface):
        self.__rating_repo = rating_repo
        self.__post_repo = post_repo

    def execute(self, post_id: int, user_id: int, score: int):
        if score not in range (0, 6):
            raise ValidationError('Score must be between 0 and 5')

        try:
            post = self.__post_repo.get_post_by_id(post_id)
            self.__rating_repo.rate_post(post_id=post.id, user_id=user_id, score=score)
        except PostModel.DoesNotExist:
            raise ValidationError('Post does not exist')