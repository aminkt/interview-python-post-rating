from rest_framework.throttling import SimpleRateThrottle

class RatePostThrottle(SimpleRateThrottle):
    scope = 'rate_post'

    def get_cache_key(self, request, view):
        # Unique cache key for each user
        return f'{self.scope}_{request.user.id}'

    def get_rate(self):
        # Rate limit: 4 requests in 30 seconds
        return '4/minute'