"""Handles parsing the data file describing the plot."""
import pkg_resources
import warnings


def parse_file(filename, parsername=''):
    """Parse plot info from given file using correct parser."""
    for ep in pkg_resources.iter_entry_points(group="uniplot.parsers"):
        try:
            parser = ep.load()
        except ImportError:
            # this parser couldn't be imported
            warnings.warn("Parser {} could not be loaded.".format(ep.name))
        except pkg_resources.UnknownExtra:
            # the extras for this parser aren't installed (not a fatal issue)
            continue

        if ep.name == parsername or parser.isfiletype(filename):
            return parser.parse(filename)
    else:
        raise ImportError("No parser could be found for {}".format(filename))
