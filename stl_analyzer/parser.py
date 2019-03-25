from dataclasses import dataclass
from typing import List, Iterator

from .exceptions import STLAnalysisException
from .model import STLSolid, Facet, Vertex, Vector

"""Parser for STL files:

Expected format:

solid [name]
  facet normal -0.785875 0 -0.618385
   outer loop
    vertex 0.360463 0 2.525
    vertex 0 0 2.98309
    vertex 0.360463 0.2 2.525
   endloop
  endfacet
  ...
endsolid


Returns:
    [type] -- [description]
"""


class LineConstants:
    FACET = 'facet'
    SEPERATOR = ' '
    NORMAL = 'normal'
    VERTEX = 'vertex'
    LOOP = 'loop'
    ENDFACET = 'endfacet'
    ENDSOLID = 'endsolid'
    ENDLOOP = 'endloop'
    FACET_DEF_PARTS = 5
    VERTEX_DEF_PARTS = 4
    SOLID_DEF_PARTS = 2


@dataclass
class FileStream(object):
    cur_line: str = None
    stream: List[str] = ()

    def next(self):
        self.cur_line = next(self.stream).strip()
        return self.cur_line


def parse_vertex(vertex_line):
    vertex_parts = vertex_line.strip().split(' ')
    if len(vertex_parts) != 4:
        raise STLAnalysisException('Bad vertex line: "{}"'.format(vertex_line))

    try:
        return Vertex(**{
            'x': float(vertex_parts[1]),
            'y': float(vertex_parts[2]),
            'z': float(vertex_parts[3]),
        })
    except ValueError:
        raise STLAnalysisException('Bad vertex value in line: "{}"'.format(vertex_line))


def parse_loop_vertices(stream: FileStream) -> List[Vertex]:
    """[summary]

    Arguments:
        stream {FileStream} -- [description]

    Returns:
        List[Vertex] -- [description]
    """
    vertices = []
    while stream.cur_line != LineConstants.ENDLOOP:
        if LineConstants.VERTEX in stream.cur_line:
            vertices.append(parse_vertex(stream.cur_line))
        stream.next()
    return vertices


def parse_facet(stream: FileStream) -> Facet:
    """Parse facet block. Expecting stream starting at facet def line

    Arguments:
        stream {FileStream} -- [description]

    Raises:
        STLAnalysisException -- [description]
        STLAnalysisException -- [description]
        STLAnalysisException -- [description]

    Returns:
        Facet -- [description]
    """
    definition_line = stream.cur_line.split(' ')
    if len(definition_line) < LineConstants.FACET_DEF_PARTS:
        raise STLAnalysisException(
            'Bad facet definition with line: "{}"'.format(
                LineConstants.SEPERATOR.join(definition_line)))

    facet_str = definition_line[0]
    normal_str = definition_line[1]
    if facet_str != LineConstants.FACET or normal_str != LineConstants.NORMAL:
        raise STLAnalysisException(
            'Bad facet definition with line: "{}"'.format(
                LineConstants.SEPERATOR.join(definition_line)))

    facet_normal = Vector(**{
        'x': float(definition_line[2]),
        'y': float(definition_line[3]),
        'z': float(definition_line[4]),
    })

    facet = Facet(normal=facet_normal, vertices=parse_loop_vertices(stream))
    if stream.next() != LineConstants.ENDFACET:
        raise STLAnalysisException(
            'Missed facet stop line {}'.format(LineConstants.ENDFACET))
    return facet


def parse_facets(stream: FileStream) -> List[Facet]:
    facets = []
    next_line = stream.next()
    while LineConstants.FACET in next_line:
        facets.append(parse_facet(stream))
        next_line = stream.next()
    return facets


def parse_solid(stl_io_stream) -> STLSolid:
    """Parse solid from stl Stream

    Arguments:
        stl_io_stream {io.Stream} -- mutable stream object of file

    Raises:
        STLAnalysisException -- [description]
    """
    stream = FileStream(stream=stl_io_stream)
    line_parts = stream.next().split(' ')
    if len(line_parts) < LineConstants.SOLID_DEF_PARTS:
        raise STLAnalysisException('Bad solid definition: "{}"'.format(line_parts))

    solid_name = line_parts[1]
    facets = parse_facets(stream)
    if LineConstants.ENDSOLID not in stream.cur_line:
        raise STLAnalysisException(
            'Bad solid definition: unexpected closing {}'.format(stream.cur_line))

    return STLSolid(name=solid_name, facets=facets)


def read_stl(full_path: str) -> Iterator[str]:
    return open(full_path, 'r')


def parse_stl_file(full_path: str) -> STLSolid:
    try:
        return parse_solid(read_stl(full_path))
    except FileNotFoundError:
        raise STLAnalysisException('STL file not found: {}'.format(full_path))
    except TypeError as e:
        raise STLAnalysisException('File error: {}'.format(str(e)))
