"""Handles the main running of the program from the command-line."""
import os
import os.path
import argparse
from . import parse, plotting
from .__about__ import __version__


def arg_setup():
    """Setup the argument parser."""
    arg_parser = argparse.ArgumentParser(
        description='Plot graphs from human-readable file formats.',
        epilog='For more detailed help see `pydoc3 uniplot`.',
    )

    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version='{} {}'.format(arg_parser.prog, __version__),
        help='display version info and exit.',
    )
    arg_parser.add_argument(
        '-s', '--style',
        help='specify a stylesheet to use for the plot.',
    )
    arg_parser.add_argument(
        '-p', '--parser',
        default='',
        help='specify the parser which should be used for the input file.',
    )
    arg_parser.add_argument(
        'input',
        help='file from which the data is read.',
    )
    arg_parser.add_argument(
        'output',
        nargs='?',
        help='name to save the output to.',
    )

    return arg_parser


def main():
    """Run the command-line program."""
    args = vars(arg_setup().parse_args())

    input_file = args['input']
    name, ext = os.path.splitext(input_file)

    plot_data = parse.parse_file(input_file, args['parser'])

    output_file = args['output']
    if output_file is None:
        output_file = name + '.pdf'

    if isinstance(plot_data, list):
        stylesheet = args['style']
    else:
        stylesheet = plot_data.get('style', args['style'])

    plotting.plot(plot_data, output_file, stylesheet)
