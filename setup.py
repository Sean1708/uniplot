import os
from setuptools import setup

base = os.path.dirname(__file__)

mdata = {}
with open(os.path.join(base, 'uniplot', '__about__.py')) as f:
    exec(f.read(), mdata)

setup(
    name=mdata['__title__'],
    version=mdata['__version__'],
    author=mdata['__author__'],
    author_email=mdata['__email__'],
    description=mdata['__description__'],
    long_description=open(os.path.join('README.rst')).read(),
    url=mdata['__homepage__'],
    download_url=mdata['__download__'],
    license=mdata['__license__'],
    packages=['uniplot', 'uniplot.parse'],

    install_requires=['HipPy', 'NumPy', 'matplotlib'],
    data_files=[(
        os.path.join(os.path.expanduser('~'), '.uniplot', 'style'),
        [
            'styles/darkgrid',
            'styles/ggplot2',
            'styles/gist',
            'styles/nogrid',
            'styles/whitegrid',
        ],
    )],
    extras_require={
        'YAML': ['PyYAML'],
        'TOML': ['PyTOML'],
    },
    entry_points={
        'console_scripts': ['uniplot = uniplot.cli:main'],
        'uniplot.parsers': [
            'hip = uniplot.parse.hip:HipParser',
            'yaml = uniplot.parse.yaml:YamlParser [YAML]',
            'toml = uniplot.parse.toml:TomlParser [TOML]',
            'multispect = uniplot.parse.multispect:MultiSpectParser',
        ],
    },
)
