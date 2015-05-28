"""Handles the main running of the program from the command-line."""
import os.path
import argparse
from .__about__ import __version__


def parser_setup():
    """Generate the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description='Plot graphs from human-readable file formats.',
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='{} {}'.format(parser.prog, __version__),
        help='display version info and exit.',
    )
    parser.add_argument(
        '--no-hip',
        action='store_true',
        help="don't write intermediate .hip file.",
    )
    parser.add_argument(
        'input',
        help='file from which the data is read.',
    )
    parser.add_argument(
        'output',
        nargs='?',
        help='name to save the output to.',
    )

    return parser


def compute_files(args):
    """Figure out which files will be written-to or read-from."""
    filename = args['input']
    name, ext = os.path.splitext(filename)
    filetype = ext[1:]
    infile = {'name': filename}
    if filetype == 'hip':
        import hippy
        infile['parser'] = hippy.decode
    elif filetype == 'yml':
        import yaml
        infile['parser'] = yaml.load
    elif filetype == 'toml':
        import pytoml
        infile['parser'] = pytoml.loads
    else:
        # TODO: some way to have arbitrary parsers
        #       I still like the whole function to test if correct filetype and
        #       function to parse, but how to load?
        raise ImportError('No module to parse {} files.'.format(filetype))

    output = args['output']
    if output is None:
        outfile = name + '.pdf'
    else:
        outfile = output

    if args['no_hip'] or filetype == 'hip':
        hipfile = None
    else:
        import hippy
        hipfile = {'name': name + '.hip', 'compiler': hippy.encode}


    return infile, outfile, hipfile


def main():
    """Run the command-line program."""
    parser = parser_setup()
    args = vars(parser.parse_args())

    # infile, outfile, hipfile = compute_files(args)
    print(compute_files(args))
