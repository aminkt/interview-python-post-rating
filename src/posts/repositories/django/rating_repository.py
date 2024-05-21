from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from posts.models import RatingModel, PostModel
from posts.repositories.interfaces.rating_repository_interface import RatingRepositoryInterface

class DjangoRatingRepository(RatingRepositoryInterface):
    def rate_post(self, post_id: int, user_id: int, score: int):
        with transaction.atomic():
            try:
                rating = self.get_user_rating_for_post(post_id=post_id, user_id=user_id)
                score_diff = score - rating.score
                rating.score = score
                rating.save()
                PostModel.objects.filter(id=post_id).update(score_sum=F('score_sum') + score_diff)
            except RatingModel.DoesNotExist:
                post = PostModel.objects.get(id=post_id)
                user = User.objects.get(id=user_id)
                rating = RatingModel(post=post, user=user, score=score)
                PostModel.objects.filter(id=post_id).update(rate_count=F('rate_count') + 1, score_sum= F('score_sum') + score)
                rating.save()

    def get_user_rating_for_post(self, post_id: int, user_id: int) -> RatingModel:
        return RatingModel.objects.get(post_id=post_id, user_id=user_id)
