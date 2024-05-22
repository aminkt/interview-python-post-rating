from django.urls import path

import posts.http.views

urlpatterns = [
    path('posts/', posts.http.views.post_list_http_handler, name='post-list'),
    path('posts/<int:post_id>/rate/', posts.http.views.rate_post_http_handler, name='post-rate'),
]
