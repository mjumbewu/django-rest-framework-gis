=======================
djangorestframework-gis
=======================

|build status|_

.. |build status| image:: https://secure.travis-ci.org/mjumbewu/django-rest-framework-gis.png
.. _build status: https://secure.travis-ci.org/mjumbewu/django-rest-framework-gis

**GeoDjango Tools for Django REST Framework**

**Author:** Mjumbe Wawatu Poe, `Follow me on Twitter <http://www.twitter.com/mjumbewu>`_.

Usage
-----

If you want to render your model as a GeoJSON ``Feature``, use the renderer.

*views.py*::

    from rest_framework.views import APIView
    from rest_framework.settings import api_settings
    from rest_framework_gis.renderers import GeoJSONRenderer
    from rest_framework_gis.parsers import GeoJSONParser

    class MyView (APIView):
        renderer_classes = (GeoJSONRenderer, ) + api_settings.DEFAULT_RENDERER_CLASSES
        parser_classes = (GeoJSONParser, ) + api_settings.DEFAULT_PARSER_CLASSES
        ...

This renderer assumes a field names ``'geometry'`` to use as the geometry field
in the ``Feature``. To use a different field, specify a ``geometry_field_name`` 
string on the view.

If you want to just use a field as a GeoJSON geometry, use the serializer field.

*serializers.py*::

    from rest_framework.serializers import ModelSerializer
    from rest_framework_gis.serializers import GeometryField
    from .models import MyModel
    
    class MySerializer (ModelSerializer):
        geometry = GeometryField()
        
        class Meta:
            model = MyModel
        
        ...

For more information about using renderers with Django REST Framework, see the
`API Guide <http://django-rest-framework.org/api-guide/renderers.html>`_ or the
`Tutorial <http://django-rest-framework.org/tutorial/1-serialization.html>`_.

Running the tests
-----------------

To run the tests against the current environment:

    ./manage.py test
