from django.urls import path

import posts.views

urlpatterns = [
    path('posts/', posts.views.post_list_http_handler, name='post-list'),
    path('posts/<int:post_id>/rate/', posts.views.rate_post_http_handler, name='post-rate'),
]
