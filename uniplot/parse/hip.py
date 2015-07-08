"""Parses Hip files."""
import hippy
import hippy.__about__
import os.path


class HipParser:

    """Parses Hip files for uniplot.

    Syntax and other information: {}
    """.format(hippy.__about__.__homepage__)

    def __init__(self, filename):
        """Set internal variables."""
        self._name = filename

    def isfiletype(self):
        """Determine if the given file is a Hip file.

        Convention is to give Hip files a '.hip' extension.
        """
        return os.path.splitext(self._name)[1] == '.hip'

    def parse(self):
        """Parse Hip file with no error handling."""
        return hippy.read(self._name)
