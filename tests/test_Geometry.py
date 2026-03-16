"""Test the ``Geometry`` class."""


class TestKeepType:
    """Test the ``keepType`` method."""

    def test_keep_type(self, geom_instance, data_regression):
        geom = geom_instance.geetools.keepType("LineString")
        geojson = geom.getInfo()
        assert geojson["type"] == "MultiLineString"
        assert geom.coordinates().getInfo() == [[[0, 1], [0, 0]]]

    def test_keep_type_point(self, geom_instance):
        geom = geom_instance.geetools.keepType("Point")
        geojson = geom.getInfo()
        assert geojson["type"] == "MultiPoint"
        assert geom.coordinates().getInfo() == [[0, 0]]

    def test_keep_type_polygon(self, geom_instance):
        geom = geom_instance.geetools.keepType("Polygon")
        geojson = geom.getInfo()
        assert geojson["type"] == "MultiPolygon"
        assert len(geom.coordinates().getInfo()) == 2

    def test_keep_type_list_single(self, geom_instance):
        geom = geom_instance.geetools.keepType(["LineString"])
        geojson = geom.getInfo()
        assert geojson["type"] == "MultiLineString"
        assert geom.coordinates().getInfo() == [[[0, 1], [0, 0]]]

    def test_keep_type_list_multiple(self, geom_instance):
        geom = geom_instance.geetools.keepType(["LineString", "Point"])
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "Point" in types
        assert "LineString" in types
        assert "Polygon" not in types

    def test_keep_type_list_all(self, geom_instance):
        geom = geom_instance.geetools.keepType(["LineString", "Point", "Polygon"])
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "Point" in types
        assert "LineString" in types
        assert "Polygon" in types


class TestRemoveType:
    """Test the ``removeType`` method."""

    def test_remove_type_point(self, geom_instance):
        geom = geom_instance.geetools.removeType("Point")
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "Point" not in types
        assert "LineString" in types
        assert "Polygon" in types

    def test_remove_type_linestring(self, geom_instance):
        geom = geom_instance.geetools.removeType("LineString")
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "LineString" not in types
        assert "Point" in types
        assert "Polygon" in types

    def test_remove_type_polygon(self, geom_instance):
        geom = geom_instance.geetools.removeType("Polygon")
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "Polygon" not in types
        assert "Point" in types
        assert "LineString" in types

    def test_remove_type_list_single(self, geom_instance):
        geom = geom_instance.geetools.removeType(["Point"])
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "Point" not in types
        assert "LineString" in types
        assert "Polygon" in types

    def test_remove_type_list_multiple(self, geom_instance):
        geom = geom_instance.geetools.removeType(["LineString", "Point"])
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        types = [g["type"] for g in geojson["geometries"]]
        assert "Point" not in types
        assert "LineString" not in types
        assert "Polygon" in types

    def test_remove_type_list_all(self, geom_instance):
        geom = geom_instance.geetools.removeType(["LineString", "Point", "Polygon"])
        geojson = geom.getInfo()
        assert geojson["type"] == "GeometryCollection"
        assert geojson["geometries"] == []
