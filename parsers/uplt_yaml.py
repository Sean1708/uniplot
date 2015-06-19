import yaml
import os.path


def isparser(filename):
    return os.path.splitext(filename)[1] == '.yml'


def parse(filename):
    with open(filename, 'r') as f:
        plot_data = yaml.load(f.read())

    return plot_data
