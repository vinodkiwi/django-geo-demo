"""
authentication app urls
"""
# third party imports
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

# local imports
from service_provider import views

router = DefaultRouter()

router.register(r'location', views.ServiceProviderView, base_name='location')


urlpatterns = [
    url(r'^', include(router.urls)),
]
