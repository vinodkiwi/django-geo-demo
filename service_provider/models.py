# third party imports
from django.db import models
from geopy import units, distance
from uszipcode import SearchEngine


def find_lat_long(zipcode):
    """
    To find latitude and longitude at given zipcode
    :param zipcode: zipcode
    :return: latitude, longitude
    """
    search = SearchEngine(simple_zipcode=True)
    zipcode = search.by_zipcode(zipcode)
    return zipcode.lat, zipcode.lng


class GeoManager(models.Manager):
    """
    Manager class used to find service provider with given either zipcode or latitude and longitude within given radius
    """
    def near_by_zip_code(self, zipcode, proximity):
        """
        Find service provider near by zipcode with distance
        :param zipcode: zipcode
        :param proximity: radius
        :return: service-provider queryset
        """
        latitude, longitude = find_lat_long(zipcode)
        rough_distance = units.degrees(arcminutes=units.nautical(kilometers=proximity)) * 2
        queryset = self.get_queryset() \
            .exclude(latitude=None) \
            .exclude(longitude=None) \
            .filter(
            latitude__range=(latitude - rough_distance, latitude + rough_distance),
            longitude__range=(longitude - rough_distance, longitude + rough_distance)
        )
        return queryset.filter(id__in=[obj.id for obj in queryset if
                                       proximity >= distance.distance((latitude, longitude),
                                                                      (obj.latitude, obj.longitude)).kilometers])

    def near_by_lat_lng(self, latitude, longitude, proximity):
        """
        Find service provider within latitude and longitude with distance
        :param latitude: latitude
        :param longitude: longitude
        :param proximity: distance
        :return: service-provider queryset
        """
        rough_distance = units.degrees(arcminutes=units.nautical(kilometers=proximity)) * 2
        queryset = self.get_queryset() \
            .exclude(latitude=None) \
            .exclude(longitude=None) \
            .filter(
            latitude__range=(latitude - rough_distance, latitude + rough_distance),
            longitude__range=(longitude - rough_distance, longitude + rough_distance)
        )
        return queryset.filter(id__in=[obj.id for obj in queryset if
                                       proximity >= distance.distance((latitude, longitude),
                                                                      (obj.latitude, obj.longitude)).kilometers])


class ServiceProvider(models.Model):
    """
    Model class store name, zipcode, latitude and longitude
    """
    name = models.CharField(max_length=127, null=True, blank=True)
    zipcode = models.CharField(max_length=127, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    objects = models.Manager()
    geo_manager = GeoManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save method() if instance has zipcode then find latitude and longitude of a zipcode.
        :param args: list or tuple arguments
        :param kwargs: keyword arguments
        :return: override save()
        """
        if getattr(self, 'zipcode', True):
            lat, lng = find_lat_long(self.zipcode)
            self.latitude = lat
            self.longitude = lng
            super(ServiceProvider, self).save(*args, **kwargs)
