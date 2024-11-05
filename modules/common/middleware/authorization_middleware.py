from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from modules.common.utils.jwt_utils import decode_token
User = get_user_model()

class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set default authentication status and user
        request.is_auth = False
        request.the_user = AnonymousUser
        request.basic_token = None  # Initialize basic_token

        # Get Authorization header
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                # Split auth type and credentials
                auth_type, credentials = auth_header.split(' ')
                auth_type = auth_type.lower()

                if auth_type == 'bearer':
                    # Existing Bearer token logic
                    user = self.get_user_from_token(credentials)
                    if user:
                        request.the_user = user
                        request.is_auth = True
                    else:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Invalid token',
                            'code': 401
                        }, status=401)
                elif auth_type == 'basic64':
                    # Store the basic auth token in request
                    request.basic_token = credentials
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid authorization type',
                        'code': 401
                    }, status=401)

            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid authorization header format',
                    'code': 401
                }, status=401)
            except AuthenticationFailed as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e),
                    'code': 401
                }, status=401)
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Authorization failed',
                    'code': 401
                }, status=401)
        else:
            # Handle case when no Authorization header is present
            return JsonResponse({
                'status': 'error',
                'message': 'Authorization header is required',
                'code': 401
            }, status=401)

        response = self.get_response(request)
        return response

    def get_user_from_token(self, token):
        """
        Validate token and return corresponding user.
        Implement your token validation logic here.
        """
        try:
            payload = decode_token(token)
            return payload.get('user_id')
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        return None