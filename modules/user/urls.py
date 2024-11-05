from django.urls import path 
from modules.user.views import UserViewset
from django_petra.router import Router, Route

routes = [
    Router.get('get/', UserViewset.get_users),
    Router.post('registration/', UserViewset.registration),
    Router.post('login/', UserViewset.login),
    Router.post('q-check', UserViewset.the_query_check)
]

urlpatterns = [eval(route) for route in Route(routes).get_all_routes()]
