"""Handles parsing the data file describing the plot."""


def parse_file(name, ext):
    """Parse the plot info from the given file."""
    if ext == '.hip':
        import hippy
        parse = hippy.decode
    elif ext == '.yml':
        import yaml
        parse = yaml.load
    elif ext == '.toml':
        import pytoml
        parse = pytoml.loads
    else:
        # TODO: some way to have arbitrary parsers
        #       I still like the whole function to test if correct filetype and
        #       function to parse, but how to load?
        raise ImportError('No module to parse {} files.'.format(ext[1:]))

    with open(name, 'r') as f:
        plot_data = parse(f.read())

    return plot_data

