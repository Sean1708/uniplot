======================
uniplot documentation!
======================

Contents:

.. toctree::
   :maxdepth: 2

   Usage
   The Data Structure <structure>
   Parsers
   Styles


.. highlight:: console

uniplot is a command line plotting utility which aims to separate a graph's data
from it's file representation. This makes it easy to re-plot graphs which were
originally plotted in other engines such as WinPlots or Origin. It also makes it
easy to plot files automatically (as part of a Makefile workflow for example).

------------
Installation
------------

uniplot is on PyPI so installation is as simple as using ``pip``::

    $ pip install uniplot

If you would rather install it from local source, I would still strongly suggest
you use ``pip`` like so::

    $ git clone https://github.com/Sean1708/uniplot.git
    $ pip install .

If you would rather not use ``pip`` then you can replace ``pip install .`` with
``python setup.py install``.

------------
Contributing
------------

Found a bug? Got a suggestion? Made some changes that you want to incorporate?
Head over to the `repo <https://github.com/Sean1708/uniplot>`_ and open an issue
or submit a pull request!
