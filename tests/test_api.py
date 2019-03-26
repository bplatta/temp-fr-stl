import unittest

import api
from stl_analyzer.exceptions import STLAnalysisException
from stl_analyzer.model import Vertex
from tests.full_path import get_full_path

class TestAPI(unittest.TestCase):
    moon_file = get_full_path(__file__, '/samples/Moon.stl')

    def test_analyze_moon_success(self):
        """
        Test analyze Moon.stl
        """
        analysis = api.analyze_stl_file(self.moon_file)
        self.assertEqual(analysis.triangle_count, 116)
        self.assertEqual(round(analysis.surface_area, 5), 7.77263)
        self.assertEqual(analysis.solid.name, 'Moon')
        expected_bounding_box = [
            Vertex(x=0.0, y=0.0, z=0.0),
            Vertex(x=0.0, y=0.0, z=3.0),
            Vertex(x=0.0, y=0.35, z=0.0),
            Vertex(x=0.0, y=0.35, z=3.0),
            Vertex(x=1.62841, y=0.0, z=0.0),
            Vertex(x=1.62841, y=0.0, z=3.0),
            Vertex(x=1.62841, y=0.35, z=0.0),
            Vertex(x=1.62841, y=0.35, z=3.0)
        ]

        for i, v in enumerate(expected_bounding_box):
            self.assertEqual(v, analysis.bounding_box[i])
