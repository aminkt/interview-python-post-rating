from typing import List, Dict, Any

from django.core.paginator import Paginator, EmptyPage

from posts.models import PostModel, RatingModel
from posts.repositories.interfaces.post_repository_interface import PostRepositoryInterface


class DjangoPostRepository(PostRepositoryInterface):
    def get_paginated_posts(self, user_id: int, page: int, page_size: int = 10) -> List[Dict[str, Any]]:
        # Query all posts
        all_posts = PostModel.objects.all()
        # Paginate the queryset
        paginator = Paginator(all_posts, page_size)
        try:
            # Get the specified page
            posts_page = paginator.page(page)
            # Extract post IDs from the paginated queryset
            post_ids = [post.id for post in posts_page.object_list]
            # Load user ratings for each post
            user_ratings = RatingModel.objects.filter(post_id__in=post_ids, user_id=user_id).values('post_id', 'score')
            # Create a dictionary to store user scores for each post
            user_scores = {rating['post_id']: rating['score'] for rating in user_ratings}

            # Combine post objects with user scores
            posts_with_user_scores = []
            for post in posts_page.object_list:
                user_score = user_scores.get(post.id, None)
                average_rating = 0
                if post.rate_count != 0:
                    average_rating = post.score_sum / post.rate_count
                posts_with_user_scores.append({
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'created_at': post.created_at,
                    'rating_count': post.rate_count,
                    'average_rating': average_rating,
                    'user_score': user_score,
                })

            return posts_with_user_scores
        except EmptyPage:
            # Handle the case when the requested page is out of range
            return []

    def get_post_by_id(self, id: int) -> PostModel:
        return PostModel.objects.get(id=id)
