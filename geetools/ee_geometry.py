"""Toolbox for the :py:class:`ee.Geometry` class."""
from __future__ import annotations

import ee

from .accessors import register_class_accessor


@register_class_accessor(ee.Geometry, "geetools")
class GeometryAccessor:
    """Toolbox for the :py:class:`ee.Geometry` class."""

    def __init__(self, obj: ee.Geometry):
        """Initialize the Geometry class."""
        self._obj = obj

    def keepType(self, type: str | list[str]) -> ee.Geometry:
        """Only keep the geometries of the given type(s) from a GeometryCollection.

        Args:
            type: The type of geometries to keep. Can be a single type or a list of types. Valid types are: Point, LineString, LinearRing, Polygon.

        Returns:
            The geometries of the given type. If a single type is provided, a Multi{type} geometry is returned. If a list of types is provided, a GeometryCollection is returned.

        Examples:
            .. jupyter-execute::

                import ee, geetools
                from geetools.utils import initialize_documentation

                initialize_documentation()

                # generate multiple geometries of different types
                point0 = ee.Geometry.Point([0,0], proj="EPSG:4326")
                point1 = ee.Geometry.Point([0,1], proj="EPSG:4326")
                poly0 = point0.buffer(1, proj="EPSG:4326")
                poly1 = point1.buffer(1, proj="EPSG:4326").bounds(proj="EPSG:4326")
                line = ee.Geometry.LineString([point1, point0], proj="EPSG:4326")
                multiPoly = ee.Geometry.MultiPolygon([poly0, poly1], proj="EPSG:4326")

                # create a geometry collection from them
                geometryCollection = ee.Algorithms.GeometryConstructors.MultiGeometry(
                    [multiPoly, poly0, poly1, point0, line],
                    crs="EPSG:4326",
                    geodesic=True,
                    maxError=1
                )

                # extract only the LineString geometries from the collection
                geom = geometryCollection.geetools.keepType('LineString')
                geom.getInfo()

            .. jupyter-execute::

                # extract LineString and Point geometries from the collection
                geom = geometryCollection.geetools.keepType(['LineString', 'Point'])
                geom.getInfo()
        """
        # will raise an error if self is not a GeometryCollection
        error_msg = "This method can only be used with GeometryCollections"
        assert self._obj.type().getInfo() == "GeometryCollection", error_msg

        types = type if isinstance(type, list) else [type]
        type_list = ee.List(types)

        def filterType(geom):
            geom = ee.Geometry(geom)
            return ee.Algorithms.If(type_list.containsAll(ee.List([geom.type()])), geom, None)

        geometries = self._obj.geometries().map(filterType, True)

        if len(types) == 1:
            return getattr(ee.Geometry, "Multi" + types[0])(geometries, self._obj.projection())

        return ee.Algorithms.GeometryConstructors.MultiGeometry(geometries, self._obj.projection())
