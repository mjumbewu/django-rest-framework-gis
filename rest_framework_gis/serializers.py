# TODO: Set the JSON package in the settings; want to use ujson
import json
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers


class GeometryField(serializers.WritableField):
    def to_native(self, obj):
        return obj.json

    def from_native(self, data):
        return GEOSGeometry(json.dumps(data))

