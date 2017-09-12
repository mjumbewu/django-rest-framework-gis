#-*- coding:utf-8 -*-
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from rest_framework.serializers import ValidationError
from rest_framework_gis.serializers import GeometryField


# TODO: Tests
#
# * Using a GeometryModelSerializer on a model with a geom
# * Using a GeometryField on a geom field in any serializer
# * Using a GeoJSONRenderer on some data
# * Using a FeatureRenderer on some data

class GeometryFieldTests (TestCase):
    def test_parsing_valid_values(self):
        field = GeometryField()

        # WKT string
        geom = field.to_internal_value('POINT(1 0)')
        self.assertEqual(geom, GEOSGeometry('POINT(1 0)'))

        # GeoJSON string
        geom = field.to_internal_value('{"type":"Point","coordinates":[1,0]}')
        self.assertEqual(geom, GEOSGeometry('{"type":"Point","coordinates":[1,0]}'))

        # GeoJSON dict
        geom = field.to_internal_value({'type': 'Point', 'coordinates': [1, 0]})
        self.assertEqual(geom, GEOSGeometry('{"type":"Point","coordinates":[1,0]}'))

        # GEOS Geometry
        geom = field.to_internal_value(GEOSGeometry('POINT(1 0)'))
        self.assertEqual(geom, GEOSGeometry('POINT(1 0)'))

    def test_parsing_invalid_values(self):
        field = GeometryField()

        # Invalid string
        with self.assertRaises(ValidationError):
            geom = field.to_internal_value('No geometry here')

        # Invalid dictionary
        with self.assertRaises(ValidationError):
            geom = field.to_internal_value({'msg': 'No geometry here'})

        # Non-dictionary
        with self.assertRaises(ValidationError):
            geom = field.to_internal_value(['No geometry here'])

        # Non-JSON-encodable obejct
        class CustomObject (object):
            pass

        with self.assertRaises(ValidationError):
            geom = field.to_internal_value(CustomObject())
