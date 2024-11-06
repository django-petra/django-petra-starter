from django.urls import path 
from modules.user.views import UserViewSet
from django_petra.router import Router, Route

routes = [
    Router.get('get/', UserViewSet.get_users),
    Router.post('registration/', UserViewSet.registration),
    Router.post('login/', UserViewSet.login),
    Router.post('q-check', UserViewSet.the_query_check)
]

urlpatterns = [eval(route) for route in Route(routes).get_all_routes()]
