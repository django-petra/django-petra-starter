from django.urls import path 
from modules.user.views import UserViewSet
from django_petra.router import Router, Route

routes = [
    Router.post('registration/', UserViewSet.registration),
    Router.post('login/', UserViewSet.login),
    Router.get('get/', UserViewSet.get_users),
    Router.get('single-user/<uuid:user_id>', UserViewSet.get_single_user),
    Router.post('q-check', UserViewSet.the_query_check),
]

urlpatterns = [eval(route) for route in Route(routes).get_all_routes()]
