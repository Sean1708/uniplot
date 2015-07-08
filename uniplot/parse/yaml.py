"""Parses YAML files."""
import yaml
import os.path


class YamlParser:

    """Parses YAML files for uniplot.

    Syntax and other information: yaml.org
    Parsing module information: https://pypi.python.org/pypi/PyYAML/
    """

    def __init__(self, filename):
        """Set internal variables."""
        self._name = filename

    def isfiletype(self):
        """Determine if the given file is a YAML file.

        Convention is to give YAML files a '.yml' extension.
        """
        return os.path.splitext(self._name)[1] == '.yml'


    def parse(self):
        """Parse YAML file with no error handling."""
        with open(self._name, 'r') as f:
            plot_data = yaml.load(f.read())

        return plot_data
