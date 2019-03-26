import unittest

from stl_analyzer import analyzer
from stl_analyzer.model import (
    Vector, Vertex, STLSolid, STLAnalysis, Facet)


class TestSTLAnalyzer(unittest.TestCase):

    @staticmethod
    def _trivial_normal():
        return Vector(0, 0, 0)

    def test_find_boundaries_points(self):
        """
        Calculate cross product of 2 vectors
        """
        vertices = [
            Vertex(5, 1, 3),
            Vertex(0, 2, 9),
            Vertex(5, 7, 1)
        ]
        facets = [
            Facet(normal=self._trivial_normal(), vertices=[
                Vertex(5, 1, 3),
                Vertex(10, 2, 9),
                Vertex(5, 71, 1)
            ]),
            Facet(normal=self._trivial_normal(), vertices=[
                Vertex(51, 0, 13),
                Vertex(7, 0, 10),
                Vertex(23, 6, 43)
            ]),
            Facet(normal=self._trivial_normal(), vertices=[
                Vertex(9, 18, 0),
                Vertex(1, 3, 71),
                Vertex(2, -5, 20)
            ])
        ]

        boundaries = analyzer.find_boundaries(facets)
        expected_bounding_box = [
            Vertex(x=1, y=-5, z=0),
            Vertex(x=1, y=-5, z=71),
            Vertex(x=1, y=71, z=0),
            Vertex(x=1, y=71, z=71),
            Vertex(x=51, y=-5, z=0),
            Vertex(x=51, y=-5, z=71),
            Vertex(x=51, y=71, z=0),
            Vertex(x=51, y=71, z=71)
        ]

        for i, v in enumerate(expected_bounding_box):
            self.assertEqual(v, boundaries[i])

    def test_calculate_cross_product(self):
        """
        Calculate cross product of 2 vectors
        """
        vector_a = Vector(4, 1, 2)
        vector_b = Vector(9, 10, 3)
        cross_product = analyzer.calculate_cross_product(vector_a, vector_b)
        expected_vector = Vector(-17, 6, 31)
        self.assertEqual(expected_vector, cross_product)


    def test_calculate_facet_area(self):
        """
        Test Calculate surface area of solid
        """
        vertices = [
            Vertex(5, 1, 3),
            Vertex(0, 2, 9),
            Vertex(5, 7, 1)
        ]
        facet = Facet(normal=self._trivial_normal(), vertices=vertices)
        expected_area = 24.71841419
        self.assertEqual(
            expected_area,
            round(analyzer.calculate_facet_area(facet), 8))

