# third party  imports
from rest_framework import serializers

# local imports
from .models import ServiceProvider


class ServiceProviderDetailSerializer(serializers.ModelSerializer):
    """
    Service provide details
    """

    class Meta:
        model = ServiceProvider
        fields = ('id', 'name')
