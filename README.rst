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

In your serializers, use the ``serializers.GeometryField`` for your geometry
fields (or use the ``serializers.GeometryModelSerializer``, which will use the
``GeometryField`` automatically). The ``GeoJSONRenderer`` will render geometry
fields as GeoJSON geometries.

Also available is the ``FeatureRenderer``, which will render a collection of
models with geometries as a GeoJSON feature collection. This renderer assumes a
field named ``'geometry'``.  To use a different field name, override the value
of the ``geometry_field_name`` attribute the renderer or the view.

For more information about using renderers with Django REST Framework, see the
`API Guide <http://django-rest-framework.org/api-guide/renderers.html>`_ or the
`Tutorial <http://django-rest-framework.org/tutorial/1-serialization.html>`_.

Running the tests
-----------------

To run the tests against the current environment:

    ./manage.py test
