from django.db import models
from django.conf import settings

class PostModel(models.Model):
    id: models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate_count = models.IntegerField(default=0)
    score_sum = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

class RatingModel(models.Model):
    id: models.IntegerField(primary_key=True)
    post = models.ForeignKey(PostModel, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'rates'
        unique_together = ('post_id', 'user')