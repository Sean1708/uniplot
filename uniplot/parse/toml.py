"""Parses TOML files."""
import pytoml
import os.path


class TomlParser:

    """Parses TOML files for uniplot.

    Syntax and other information: https://github.com/toml-lang/toml
    Parsing module information: https://github.com/avakar/pytoml
    """

    def __init__(self, filename):
        """Set internal variables."""
        self._name = filename

    def isfiletype(self):
        """Determine if the given file is a TOML file.

        Convention is to give TOML files a '.toml' extension.
        """
        return os.path.splitext(self._name)[1] == '.toml'

    def parse(self):
        """Parse TOML file with no error handling."""
        with open(self._name, 'r') as f:
            plot_data = pytoml.load(f)

        return plot_data
