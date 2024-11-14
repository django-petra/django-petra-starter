from django.urls import path 
from modules.user.views import UserViewSet
from django_petra.router import Router, Route

API_VERSION = 'v1'
urlpatterns = []


routes = [
    Router.post('registration/', UserViewSet.registration),
    Router.post('login/', UserViewSet.login),
    Router.get('users/', UserViewSet.get_users),

    Router.get('users/<uuid:user_id>', UserViewSet.get_single_user),
    Router.delete('users/<uuid:user_id>', UserViewSet.delete_user),
    Router.put('users/<uuid:user_id>', UserViewSet.update_user),
    Router.post('q-check', UserViewSet.the_query_check),
]

urlpatterns = [eval(route) for route in Route(routes).get_all_routes()]
