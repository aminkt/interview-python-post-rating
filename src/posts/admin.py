from django.contrib import admin

from posts.storage.models import PostModel
from posts.storage.models import RatingModel

admin.site.register(PostModel)
admin.site.register(RatingModel)
