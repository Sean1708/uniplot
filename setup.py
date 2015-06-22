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
    packages=['uniplot'],

    install_requires=['HipPy', 'matplotlib'],
    data_files=[
        (
            os.path.join(os.path.expanduser('~'), '.uniplot', 'parser'),
            ['parsers/uplt_yaml.py', 'parsers/uplt_toml.py'],
        ),
        (
            os.path.join(os.path.expanduser('~'), '.uniplot', 'style'),
            [
                'styles/darkgrid',
                'styles/ggplot2',
                'styles/gist',
                'styles/nogrid',
                'styles/whitegrid',
            ],
        )
    ],
    entry_points={'console_scripts': ['uniplot = uniplot.cli:main']},
)
