# TODO: Set the JSON package in the settings; want to use ujson
import json
from django.contrib.gis.gdal.error import GDALException
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models
from rest_framework import serializers


class GeometryField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        if isinstance(data, GEOSGeometry):
            return data

        # If the data is not already a string, try to dump it to a string using
        # a JSON serializer.
        if isinstance(data, (str, bytes)):
            str_data = data
        else:
            try:
                str_data = json.dumps(data)
            except TypeError:
                raise serializers.ValidationError('Value must be a geometry string, or JSON-serializable GeoJSON dict. Got: {!r}'.format(data))

        # Try to construct a geometry from the string data, raising
        # ValidationError if not possible.
        try:
            geom = GEOSGeometry(str_data)
        except ValueError:
            raise serializers.ValidationError('Value not recognized as WKT, EWKT, HEXEWKB, or GeoJSON: {!r}'.format(data))
        except GDALException:
            raise serializers.ValidationError('Value does not represent a valid geometry: {!r}'.format(data))

        # Return the resulting geometry.
        return geom


class GeometryModelSerializer (serializers.ModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        models.GeometryField: GeometryField,
    }