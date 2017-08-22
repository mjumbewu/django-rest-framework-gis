# TODO: Set the JSON package in the settings; want to use ujson
from collections import OrderedDict
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

# QUESTION: Should the setting be called DEFAULT_GEOMETRY_FIELD_NAME or namespaced in the rest-framework settings?
DEFAULT_GEOMETRY_FIELD_NAME = getattr(settings, 'DEFAULT_GEOMETRY_FIELD_NAME', 'geometry')


class GeoJSONEncoder (JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GEOSGeometry):
            return json.loads(obj.json)  #FIXME: is there a better way to do this?
        else:
            return super(GeoJSONEncoder, self).default(obj)


class GeoJSONRenderer(JSONRenderer):
    """
    Renderer which serializes geometries to GeoJSON
    """

    encoder_class = GeoJSONEncoder
    media_type = 'application/json'
    format = 'geojson'


class FeatureRenderer(GeoJSONRenderer):
    """
    GeoJSON renderer which serializes specifically to GeoJSON features or
    feature collections
    """

    geometry_field = DEFAULT_GEOMETRY_FIELD_NAME

    def render(self, data, media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        geom_field = getattr(renderer_context.get('view'), 'geometry_field_name',
                             DEFAULT_GEOMETRY_FIELD_NAME)

        if isinstance(data, list):
            new_data = OrderedDict([
                ('type', 'FeatureCollection'),
                ('features', [(self.get_feature(elem, geom_field) or elem) for elem in data]),
            ])
        else:
            new_data = self.get_feature(data) or data

        return super(FeatureRenderer, self).render(new_data, media_type, renderer_context)

    def get_feature(self, data, geom_field):
        if geom_field not in data:
            return None

        geometry = data.pop(geom_field)

        if isinstance(geometry, basestring):
            geometry = GEOSGeometry(geometry)

        feature = OrderedDict([
          ('type', 'Feature'),
          ('geometry', geometry),
          ('properties', data),
        ])

        return feature
