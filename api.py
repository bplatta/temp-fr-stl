from functools import reduce

from stl_analyzer.parser import parse_stl_file
from stl_analyzer.validator import validate_stl_data
from stl_analyzer.analyzer import analyze_stl_data
from stl_analyzer.model import STLAnalysis
from stl_analyzer.exceptions import STLAnalysisException


def compose(*functions):
    funcs_reversed = functions[::-1]

    def _compose_2(f, g):
        return lambda x: f(g(x))

    return reduce(_compose_2, funcs_reversed, lambda x: x)


def analyze_stl_file(full_path: str) -> STLAnalysis:
    """Analyze stl file

    Arguments:
        full_path {str}

    Returns:
        STLAnalysis
    """
    try:
        return compose(
            parse_stl_file,
            validate_stl_data,
            analyze_stl_data)(full_path)
    except STLAnalysisException as e:
        print(str(e))


def view_analysis(analysis: STLAnalysis):
    """Run analysis and display print
    Arguments:
        full_path {str} -- path to stl file
    """
    if analysis:
        analysis.print()
