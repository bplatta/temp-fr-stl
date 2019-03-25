from typing import List
from itertools import product as cartesian_product

from .model import STLAnalysis, STLSolid, Facet, Vector, Vertex
from .exceptions import STLAnalysisException


def find_boundaries(facets: List[Facet]) -> List[Vertex]:
    facet_vertices = [facet.vertices for facet in facets]
    all_x = [vertex.x for vertices in facet_vertices for vertex in vertices]
    all_y = [vertex.y for vertices in facet_vertices for vertex in vertices]
    all_z = [vertex.z for vertices in facet_vertices for vertex in vertices]

    return [
        Vertex(*vertex)
        for vertex in cartesian_product(
            (min(all_x), max(all_x)),
            (min(all_y), max(all_y)),
            (min(all_z), max(all_z))
        )]


def calculate_vector(vertex_a, vertex_b):
    return Vector(
        x=vertex_b.x - vertex_a.x,
        y=vertex_b.y - vertex_a.y,
        z=vertex_b.z - vertex_a.z)


def calculate_cross_product(vector_a: Vector, vector_b: Vector) -> Vector:
    return Vector(
        x=vector_a.y * vector_b.z - vector_a.z * vector_b.y,
        y=vector_a.z * vector_b.x - vector_a.x * vector_b.z,
        z=vector_a.x * vector_b.y - vector_a.y * vector_b.x)


def calculate_facet_area(facet: Facet) -> float:
    """Calculate the area of a facet area (triangle)

    Arguments:
        facet {Facet} -- facet.vertices

    Raises:
        STLAnalysisException

    Returns:
        float
    """

    if len(facet.vertices) != 3:
        raise STLAnalysisException(
            'Unexpected facet shape: {} vertices'.format(len(facet.vertices)))

    vertex_1 = facet.vertices[0]
    vertex_2 = facet.vertices[1]
    vertex_3 = facet.vertices[2]
    vector_1_2 = calculate_vector(vertex_1, vertex_2)
    vector_1_3 = calculate_vector(vertex_1, vertex_3)
    return (
        calculate_cross_product(vector_1_2, vector_1_3)
    ).length / 2


def analyze_stl_data(stl_solid: STLSolid) -> STLAnalysis:
    return STLAnalysis(
        solid=stl_solid,
        triangle_count=len(stl_solid.facets),
        surface_area=sum(map(calculate_facet_area, stl_solid.facets)),
        bounding_box=find_boundaries(stl_solid.facets))
