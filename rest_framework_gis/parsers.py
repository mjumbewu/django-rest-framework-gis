import json
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError

# TODO: This should come from the settings, as we need it in multiple places.
DEFAULT_GEOMETRY_FIELD_NAME = 'geometry'

class GeoJSONParser(JSONParser):
    """
    Parses GeoJSON data.
    """

    media_type = 'application/json'

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(GeoJSONParser, self).parse(stream, media_type, parser_context)
        
        # TODO: Test this!!!
        
        parser_context = parser_context or {}
        geom_field = getattr(parser_context.get('view'), 'geometry_field_name', 
                             DEFAULT_GEOMETRY_FIELD_NAME)
        
        try:
            geometry = data['geometry']
        except KeyError:
            raise ParseError('Invalid GeoJSON feature - "geometry" attribute not found in %s' % data.keys())
        
        try:
            properties = data['properties']
        except KeyError:
            raise ParseError('Invalid GeoJSON feature - "properties" attribute not found in %s' % data.keys())
        
        properties[geom_field] = geometry
        return properties

