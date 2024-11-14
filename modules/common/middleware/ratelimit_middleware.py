from django.core.cache import cache
from django.http import JsonResponse
import time
from django.conf import settings

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = getattr(settings, 'RATE_LIMIT_PER_MINUTE', 60)
        self.window_size = 60  # 1 minute window
        
    def __call__(self, request):
        # Get client IP and API path
        client_ip = self.get_client_ip(request)
        api_path = request.path.strip('/')  # Remove leading/trailing slashes
        
        # Check rate limit for this specific API endpoint
        if self.is_rate_limited(client_ip, api_path):
            return JsonResponse({
                "status": "error",
                "message": "Rate limit exceeded. Please try again later",
                "code": 429,
                "path": api_path
            }, status=429)
            
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Get client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
    
    def is_rate_limited(self, client_ip, api_path):
        """Check if request should be rate limited for specific API"""
        # Create unique cache key for this IP + API combination
        cache_key = f"rate_limit:{client_ip}:{api_path}"
        current_time = time.time()
        
        # Get request history from cache
        request_history = cache.get(cache_key, [])
        
        # Remove requests outside current window
        request_history = [t for t in request_history 
                         if t > current_time - self.window_size]
        
        # Check if rate limit is exceeded
        if len(request_history) >= self.rate_limit:
            return True
            
        # Add current request
        request_history.append(current_time)
        cache.set(cache_key, request_history, self.window_size)
        
        return False