# TODO: Set the JSON package in the settings; want to use ujson
import json
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models
from rest_framework import serializers


class GeometryField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return GEOSGeometry(json.dumps(data))


class GeometryModelSerializer (serializers.ModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        models.GeometryField: GeometryField,
    }