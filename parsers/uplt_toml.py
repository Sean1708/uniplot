import pytoml
import os.path


def isparser(filename):
    return os.path.splitext(filename)[1] == '.toml'


def parse(filename):
    with open(filename, 'r') as f:
        plot_data = pytoml.load(f)

    return plot_data
