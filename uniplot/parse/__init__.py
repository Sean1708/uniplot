"""Handles parsing the data file describing the plot."""
import pkg_resources
import warnings
import os.path
import errno
import os

from .. import plotting


def parse_file(filename, parsername=''):
    """Parse plot info from given file using correct parser."""
    if not os.path.exists(filename):
        num = errno.ENOENT
        raise FileNotFoundError(num, os.strerror(num), filename)
    elif parsername == '':
        data = find_parser(filename)
    else:
        data = load_parser(filename, parsername)

    return plotting.Graph(data)


def find_parser(filename):
    """Find the correct parser by iterating entry_points."""
    for ep in pkg_resources.iter_entry_points(group='uniplot.parsers'):
        try:
            parser = ep.load()(filename)
        except ImportError:
            # this parser couldn't be imported
            warnings.warn("parser '{}' could not be loaded".format(ep.name))
            continue
        except pkg_resources.DistributionNotFound:
            # this parser wasn't installed
            continue

        if parser.isfiletype():
            return parser.parse()
    else:
        raise ImportError("no parser could be found for '{}'".format(filename))


def load_parser(filename, parsername):
    """Load only the specified entrypoint."""
    eps = list(pkg_resources.iter_entry_points(
        group='uniplot.parsers', name=parsername
    ))
    if len(eps) > 1:
        warnings.warn("multiple parsers called '{}'".format(parsername))
    elif len(eps) < 1:
        raise ImportError("parser '{}' could not be found".format(parsername))

    errors = []
    for ep in eps:
        try:
            parser = ep.load()(filename)
            return parser.parse()
        except Exception as e:
            errors.append(e)
    else:
        import traceback
        import sys

        for err in errors:
            print('-'*60, file=sys.stderr)
            traceback.print_exception(err.__class__, err, err.__traceback__)

        print(
            '-'*60,
            "no parser named '{}' could successfully parse '{}'".format(
                parsername, filename
            ),
            'tracebacks have been printed above for extra information',
            sep='\n',
            file=sys.stderr,
        )

        sys.exit(1)
