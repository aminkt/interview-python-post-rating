import datetime
from typing import List

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import F

from posts.domain.repository_interfaces import RatingRepositoryInterface
from posts.storage.models import RatingModel, PostModel


class DjangoRatingRepository(RatingRepositoryInterface):
    def apply_pending_rates(self, rate_ids: List[int]):
        ratings = RatingModel.objects.filter(id__in=rate_ids, is_applied=False).all()
        post_rate_changes = {}
        applied_ids = []
        for rate in ratings:
            try:
                post_changes = post_rate_changes[rate.post_id]
            except KeyError:
                post_changes = {'rate_count': 0, 'score_sum': 0}

            rate_count = post_changes['rate_count']
            score_sum = post_changes['score_sum']
            if rate.old_score is None:
                rate_count += 1
                score_sum += rate.score
            else:
                score_sum += rate.score - rate.old_score

            post_rate_changes[rate.post_id] = {
                'rate_count': rate_count,
                'score_sum': score_sum
            }
            applied_ids.append(rate.id)

        for post_id in post_rate_changes:
            item = post_rate_changes[post_id]
            PostModel.objects.filter(id=post_id).update(
                rate_count=F('rate_count') + item['rate_count'],
                score_sum=F('score_sum') + item['score_sum']
            )

        RatingModel.objects.filter(id__in=applied_ids).update(is_applied=True)

    def get_queued_rate_ids(self, page: int) -> List[int]:
        try:
            date_time = datetime.datetime.now() - datetime.timedelta(hours=6)
            query = RatingModel.objects.filter(created_at__lte=date_time, is_applied=False).values_list('id', flat=True)
            paginator = Paginator(query, 500)
            return paginator.page(page)
        except EmptyPage:
            return []

    def queue_rate_for_delayed_effect(self, post_id: int, user_id: int, score: int):
        with transaction.atomic():
            try:
                rating = self.get_user_rating_for_post(post_id=post_id, user_id=user_id)
                # In cases user want to change his rate, but it is not effected yet and old score is settled,
                # we don't need to change old_score.
                if rating.is_applied:
                    rating.old_score = rating.score
                rating.score = score
                rating.is_applied = False
                rating.save()
            except RatingModel.DoesNotExist:
                post = PostModel.objects.get(id=post_id)
                user = User.objects.get(id=user_id)
                rating = RatingModel(post=post, user=user, score=score, is_applied=False)
                rating.save()

    def rate_post(self, post_id: int, user_id: int, score: int):
        with transaction.atomic():
            try:
                rating = self.get_user_rating_for_post(post_id=post_id, user_id=user_id)
                if rating.is_applied:
                    rating.old_score = rating.score
                rating.score = score
                rating.is_applied = True
                rating.save()

                if not rating.old_score:
                    # If old score has not valued, change effect post rate count too.
                    PostModel.objects.filter(id=post_id).update(
                        rate_count=F('rate_count') + 1,
                        score_sum=F('score_sum') + rating.score
                    )
                else:
                    # else difference of old value and new value will affect on post rate score sum.
                    PostModel.objects.filter(id=post_id).update(score_sum=F('score_sum') + (rating.score - rating.old_score))
            except RatingModel.DoesNotExist:
                # And if not rated before, both score and count in the post will change.
                post = PostModel.objects.get(id=post_id)
                user = User.objects.get(id=user_id)
                rating = RatingModel(post=post, user=user, score=score, is_applied=True)
                PostModel.objects.filter(id=post_id).update(
                    rate_count=F('rate_count') + 1,
                    score_sum=F('score_sum') + rating.score
                )
                rating.save()

    def get_user_rating_for_post(self, post_id: int, user_id: int) -> RatingModel:
        return RatingModel.objects.get(post_id=post_id, user_id=user_id)
