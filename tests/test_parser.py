import unittest
import os.path

from stl_analyzer import parser
from stl_analyzer.exceptions import STLAnalysisException
from stl_analyzer.model import Vertex, Vector
from tests.full_path import get_full_path


class TestSTLParser(unittest.TestCase):
    file_simple = get_full_path(__file__, '/samples/simple.stl')
    invalid_solid = get_full_path(__file__, '/samples/invalid_solid.stl')
    invalid_facet = get_full_path(__file__, '/samples/invalid_facet.stl')
    invalid_vertices = get_full_path(__file__, '/samples/invalid_vertices.stl')
    invalid_vertices_types = get_full_path(__file__, '/samples/invalid_vertices_type.stl')

    def test_parse_stl_file_success(self):
        """
        Test parse STL simple file to Solid
        """
        solid = parser.parse_stl_file(self.file_simple)
        self.assertEqual('simple', solid.name)
        expected_normal = Vector(0, 0, 0)
        facet_1 = solid.facets[0]
        facet_2 = solid.facets[1]

        self.assertEqual(facet_1.normal, expected_normal)
        self.assertEqual(facet_2.normal, expected_normal)

        facet_1_vertices = facet_1.vertices
        self.assertEqual(facet_1_vertices[0], Vertex(0.0, 0.0, 0.0))
        self.assertEqual(facet_1_vertices[1], Vertex(1.0, 0.0, 0.0))
        self.assertEqual(facet_1_vertices[2], Vertex(1.0, 1.0, 1.0))
        
        facet_2_vertices = facet_2.vertices
        self.assertEqual(facet_2_vertices[0], Vertex(0.0, 0.0, 0.0))
        self.assertEqual(facet_2_vertices[1], Vertex(0.0, 1.0, 1.0))
        self.assertEqual(facet_2_vertices[2], Vertex(1.0, 1.0, 1.0))


    def test_parse_stl_file_invalid_solid(self):
        """
        Test parse Invalid Solid definition
        """
        try:
            solid = parser.parse_stl_file(self.invalid_solid)
            self.fail('Failed to raise bad solid def')
        except STLAnalysisException as e:
            self.assertEqual('Bad solid definition: "solid"', str(e))

    def test_parse_stl_file_invalid_facet_normal(self):
        """
        Test parse Invalid facet definition
        """
        try:
            solid = parser.parse_stl_file(self.invalid_facet)
            self.fail('Failed to raise bad facet normal def')
        except STLAnalysisException as e:
            self.assertEqual('Bad facet definition with line: "facet 0 0 0"', str(e))

    def test_parse_stl_file_invalid_facet_vertices_types(self):
        """
        Test parse Invalid facet vertices types
        """
        try:
            solid = parser.parse_stl_file(self.invalid_vertices_types)
            self.fail('Failed to raise bad facet vertex type')
        except STLAnalysisException as e:
            self.assertEqual('Bad vertex value in line: "vertex not 0 0"', str(e))


    def test_parse_stl_file_invalid_facet_vertices_count(self):
        """
        Test parse Invalid facet vertices counts
        """
        try:
            solid = parser.parse_stl_file(self.invalid_vertices)
            self.fail('Failed to raise bad facet vertices count')
        except STLAnalysisException as e:
            self.assertEqual('Bad vertex line: "vertex 1 0"', str(e))

    def test_parse_stl_file_does_not_exist(self):
        """
        Test parse invalid stl file does not exist
        """
        try:
            solid = parser.parse_stl_file('not/a/thing')
            self.fail('Failed to raise file does not exist')
        except STLAnalysisException as e:
            self.assertEqual('STL file not found: not/a/thing', str(e))
