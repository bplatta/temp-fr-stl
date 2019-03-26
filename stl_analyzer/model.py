import math

from typing import List
from dataclasses import dataclass


def is_coordinate_equal(obj1, obj2):
    return obj1.x == obj2.x and obj1.y == obj2.y and obj1.z == obj2.z


@dataclass
class Vector(object):
    x: float
    y: float
    z: float

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Vector):
            return is_coordinate_equal(self, other)
        return False

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


@dataclass
class Vertex(object):
    x: float
    y: float
    z: float

    def __str__(self):
        return '[x:{},y:{},z:{}]'.format(self.x, self.y, self.z)
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Vertex):
            return is_coordinate_equal(self, other)
        return False


@dataclass
class Facet(object):
    normal: Vector
    vertices: List[Vertex]


@dataclass
class STLSolid(object):
    name: str
    facets: List[Facet]


@dataclass
class STLAnalysis(object):
    solid: STLSolid
    triangle_count: int
    surface_area: float
    bounding_box: List[Vertex]

    def print(self):
        print('Analysis for solid {} >>>'.format(self.solid.name))
        print('Number of triangles: {}'.format(self.triangle_count))
        print('Surface Area: {}'.format(self.surface_area))
        print('Bounding Box: {}'.format(self.bounding_box))
