"""Parses YAML files."""
import yaml
import os.path


def isfiletype(filename):
    return os.path.splitext(filename)[1] == '.yml'


def parse(filename):
    with open(filename, 'r') as f:
        plot_data = yaml.load(f.read())

    return plot_data
