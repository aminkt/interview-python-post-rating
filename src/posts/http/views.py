from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from posts.domain.exceptions import ValidationError
from posts.domain.use_cases import RatePostUseCase
from posts.http.throttles import RatePostThrottle
from project.dependencies import Dependencies
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@login_required()
def post_list_http_handler(request):
    user_id = request.user.id
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    result = Dependencies.post_repository().get_paginated_posts(user_id, page, page_size)
    return Response(data=result, status=HTTP_200_OK)


@api_view(['POST'])
@login_required()
@throttle_classes([RatePostThrottle])
def rate_post_http_handler(request, post_id):
    try:
        RatePostUseCase(
            rating_repo=Dependencies.rating_repository(),
            post_repo=Dependencies.post_repository()
        ).execute(post_id=post_id, user_id=request.user.id, score=request.data['score'])

        return Response(data={'success': True, 'message': 'Rating submitted successfully.'}, status=HTTP_200_OK)
    except ValidationError as e:
        return Response(data={'success': False, 'message': e.args[0]}, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(e, exc_info=True)
        return Response(data={'success': False, 'message': 'Something went wrong!'}, status=HTTP_500_INTERNAL_SERVER_ERROR)