"""Handles the main running of the program from the command-line."""
import os.path
import argparse
from . import parsing, plotting
from .__about__ import __version__


def arg_setup():
    """Setup the argument parser."""
    arg_parser = argparse.Argumentarg_Parser(
        description='Plot graphs from human-readable file formats.',
    )

    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version='{} {}'.format(arg_parser.prog, __version__),
        help='display version info and exit.',
    )
    arg_parser.add_argument(
        '--no-hip',
        action='store_true',
        help="don't write intermediate .hip file.",
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

    plot_data = parsing.parse_file(input_file, ext)

    output_file = args['output']
    if output_file is None:
        output_file = name + '.pdf'

    plotting.plot(plot_data, output_file)

    if not args['no_hip'] and ext != '.hip':
        import hippy
        hippy.write(name+'.hip', plot_data)
