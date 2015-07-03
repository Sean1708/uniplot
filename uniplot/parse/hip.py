"""Parses Hip files."""
import hippy
import os.path


def isfiletype(filename):
    return os.path.splitext(filename)[1] == '.hip'

def parse(filename):
    return hippy.read(filename)
