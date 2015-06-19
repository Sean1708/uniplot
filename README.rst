=======
uniplot
=======

``uniplot`` is simple utility which aims to unify plotting. The issue with modern
plotting programs such as EasyPlot and Origin (apart from the fact you have to
pay for them D:) is that they all use a different format to represent their
plots, meaning you have to have all the programs installed on your computer to
use these plots (an even bigger issue since these plots never seem to be
exportable to images). ``uniplot`` aims to seperate the plot data from the data
representation so that any file format can be used (as long as a parser exists)
and you can even write your graphs by hand if you wish.

uniplot is written in Python meaning it's cross-platform, easy to install and
will always be free (both as in speech and as in beer).

.. _`Hip`: https://github.com/mario-deluna/Hip

------------
Installation
------------

uniplot is currently not available on PyPI but installation is still as simple
as cloning the `repo`_ and using ``pip``::

    $ git clone https://github.com/Sean1708/uniplot.git
    $ pip install .

.. _`repo`: https://github.com/Sean1708/uniplot

-----
Usage
-----

To get an up-to-date overview of all flags use the ``--help`` option.

.. code:: console

    $ uniplot --help

The simplest usage of ``uniplot`` is to supply a single file name, this will use
that file to plot the graph (automatically guessing the file format) and save it
as a PDF using the original file name as a base. For example

.. code:: console

    $ uniplot graphs/AwesomeData.hip

will create a PDF in ``graphs`` called ``AwesomeData.pdf``. By supplying a
second file name you can specify the file name, location and type.

.. code:: console

    $ uniplot graphs/AwesomeData.yml plots/AwesomePlot.png

This will create a PNG in ``plots`` called ``AwesomePlot.png``.

``uniplot`` uses ``matplotlib`` as a backend so to get a list of the filetypes
(with their extensions) that you can save as run the following in a Python
interpreter:

.. code:: pycon

    >>> from matplotlib import pyplot
    >>> fig = pyplot.figure()
    >>> print(fig.canvas.get_supported_filetypes())
    {'bmp': 'Windows bitmap',
    'eps': 'Encapsulated Postscript',
    'gif': 'Graphics Interchange Format',
    'jpeg': 'JPEG',
    'jpg': 'JPEG',
    'pdf': 'Portable Document Format',
    'pgf': 'PGF code for LaTeX',
    'png': 'Portable Network Graphics',
    'ps': 'Postscript',
    'raw': 'Raw RGBA bitmap',
    'rgba': 'Raw RGBA bitmap',
    'svg': 'Scalable Vector Graphics',
    'svgz': 'Scalable Vector Graphics',
    'tif': 'Tagged Image Format File',
    'tiff': 'Tagged Image Format File'}

------------------
The Data Structure
------------------

I'll write it soon I promise!

-----------------------
Writing Your Own Parser
-----------------------

Ditto.
