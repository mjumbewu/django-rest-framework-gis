# TODO: Set the JSON package in the settings; want to use ujson
import json
from rest_framework.renderers import JSONRenderer
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

# QUESTION: Should the setting be called DEFAULT_GEOMETRY_FIELD_NAME or namespaced in the rest-framework settings?
DEFAULT_GEOMETRY_FIELD_NAME = getattr(settings, 'DEFAULT_GEOMETRY_FIELD_NAME', 'geometry')

class GeoJSONRenderer(JSONRenderer):
    """
    Renderer which serializes to GeoJSON
    """

    media_type = 'application/json'
    format = 'json'
    geometry_field = DEFAULT_GEOMETRY_FIELD_NAME
    

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders *data* into a GeoJSON feature.
        """
        renderer_context = renderer_context or {}
        geom_field = getattr(renderer_context.get('view'), 'geometry_field_name', 
                             DEFAULT_GEOMETRY_FIELD_NAME)
        
        if isinstance(data, list):
            new_data = {
              'type': 'FeatureCollection',
              'features': [(self.get_feature(elem, geom_field) or elem) for elem in data]
            }
        else:
            new_data = self.get_feature(data) or data

        return super(GeoJSONRenderer, self).render(new_data, media_type, renderer_context)
    
    def get_feature(self, data, geom_field):
        if geom_field not in data:
            return None
        
        geometry = data.pop(geom_field)
        
        if isinstance(geometry, basestring):
            geometry = GEOSGeometry(geometry)
            
        feature = {
          'type': 'Feature',
          'geometry': json.loads(geometry.json), #FIXME: is there a better way to do this?
          'properties': data,
        }
        
        return feature
