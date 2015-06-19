"""Handles parsing the data file describing the plot."""
import os
import os.path
import sys
import hippy
import warnings
import importlib


def parse_file(name, ext):
    """Parse plot info from given file using correct parser."""
    # quickly load Hip files
    if ext == '.hip':
        return hippy.read(name)

    # otherwise load parsers until the correct one is found
    parser_dir = os.path.join(os.path.expanduser('~'), '.uniplot', 'parser')
    parser_files = os.listdir(parser_dir)
    sys.path.append(parser_dir)

    for pf in parser_files:
        parser_mod = importlib.import_module(
            os.path.splitext(os.path.basename(pf))[0]
        )

        if parser_mod.isparser(name):
            parse = parser_mod.parse
            break
    else:
        m = 'No module to parse {} files, defaulting to HipPy.'.format(ext[1:])
        warnings.warn(m)
        parse = hippy.decode

    plot_data = parse(name)

    return plot_data
