# python imports

# third party imports
from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.response import Response

# local imports
from .models import ServiceProvider
from .serializers import ServiceProviderDetailSerializer


class ServiceProviderView(viewsets.ModelViewSet):
    serializer_class = ServiceProviderDetailSerializer
    queryset = ServiceProvider.objects.all()
    http_method_names = ('get',)

    @action(methods=('get', ), detail=False, url_name='by-zip-code', url_path='by-zip-code')
    def by_zipcode(self, request):
        zipcode = request.GET.get('zipcode', None)
        distance = request.GET.get('distance', None)
        service_provider_qs = ServiceProvider.geo_manager.near_by_zip_code(zipcode, float(distance))
        serializer = self.serializer_class(service_provider_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('get',), detail=False, url_name='by-lat-lng', url_path='by-lat-lng')
    def by_lat_lng(self, request):
        lat = request.GET.get('lat', None)
        lng = request.GET.get('lng', None)
        distance = request.GET.get('distance', None)
        service_provider_qs = ServiceProvider.geo_manager.near_by_lat_lng(float(lat), float(lng), float(distance))
        serializer = self.serializer_class(service_provider_qs, many=True)
        return Response(serializer.data)
