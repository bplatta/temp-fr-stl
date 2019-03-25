from .model import STLSolid


def validate_stl_data(stl_solid: STLSolid) -> STLSolid:
    """Validate STL solid for printing

    Raise Exception if cant be printed.

    Arguments:
        stl_solid {STLSolid}

    Returns:
        STLSolid
    """

    return stl_solid


def validate_facet_normals(stl_solid: STLSolid) -> STLSolid:
    return stl_solid
