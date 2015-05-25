import argparse
from .__about__ import __version__


def main():
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
        'input',
        help='file from which the data is read.',
    )
    parser.add_argument(
        'output',
        nargs='?',
        help='name to save the output to.',
    )

    args = parser.parse_args()
    print(vars(args))
