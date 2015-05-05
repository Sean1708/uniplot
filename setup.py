import uniplot
from setuptools import setup

setup(
    name=uniplot.__title__,
    version=uniplot.__version__,
    author=uniplot.__author__,
    author_email=uniplot.__email__,
    description=uniplot.__description__,
    long_description=open('README.rst').read(),
    url=uniplot.__homepage__,
    download_url=uniplot.__download__,
    install_requires=['hippy', 'matplotlib'],
    packages=['refile'],
)
