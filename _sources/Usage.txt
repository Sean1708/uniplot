.. highlight:: console

=====
Usage
=====

You can get an up-to-date overview of flags and usage with the ``--help``
option::

    $ uniplot --help

For a more in-depth help you can browse the main uniplot docstring::

    $ pydoc uniplot

The simplest usage of uniplot is to supply a single file name, this will use
that file to plot the graph (automatically guessing the file format) and save it
as a PDF using the orignal file name and location. For example::

    $ uniplot graphs/AwesomeGraph.hip

will create a PDF in :file:`graphs` called :file:`AwesomeData.pdf`. By supplying
a second file name you can specify the file type, location and name::

    $ uniplot graphs/AwesomeGraph.yml plots/AwesomePlot.png

This will create a PNG in :file:`plots` called :file:`AwesomePlot.png`.

uniplot uses matplotlib as a backend so to get a list of the file types (with
their extensions) that you can save as run the following in a Python
interpreter:

.. code-block:: python

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

-----------------
Using Stylesheets
-----------------

matplotlib allows you to define `stylesheets`_ so that you can easily adapt your
graphs to your liking. uniplot takes advantage of this functionality and also
allows you to use your own stylesheets. To do so you must put your stylesheet in
:file:`$HOME/.uniplot/style` then use it by supplying the filename to the ``-s``
flag. For example if you wrote a stylesheet called ``uber_mega_style`` you would
write it in :file:`$HOME/.uniplot/style/uber_mega_style` and call it like so::

    $ uniplot -s uber_mega_style my_graph.hip

alternatively you can give your top-level graph a ``style`` attribute (see
:ref:`graph`):

.. code-block:: yaml

   style: "uber_mega_style"
   graphs: ...

matplotlib comes with some predefined stylesheets which can be used, to see
which ones are installed on your system use the following python snippet:

.. code-block:: python

   >>> from matplotlib import pyplot
   >>> print(pyplot.style.available)
   ['dark_background', 'ggplot', 'grayscale', 'bmh', 'fivethirtyeight']

uniplot also comes with some predefined styles, shamelessly stolen from
`ctokheim`_, which are placed in :file:`$HOME/.uniplot/style`. If you're
interested in writing your own I suggest you start here since the matplotlib
documentation is quite lacking.

.. _`stylesheets`: http://matplotlib.org/users/style_sheets.html#defining-your-own-style
.. _`ctokheim`: https://github.com/ctokheim/matplotlibrc
