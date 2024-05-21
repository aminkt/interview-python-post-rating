from django.contrib import admin

from posts.models import PostModel
from posts.models import RatingModel

admin.site.register(PostModel)
admin.site.register(RatingModel)
