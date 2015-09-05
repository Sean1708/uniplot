==================
The Data Structure
==================

One of the main aims of uniplot is to separate plot data from it's
representation. As such a plot data structure has been defined, which will be
described on this page.

The data structure is split into three main data structures (that will
eventually make sense I promise):

Graph
    The ``graph`` is the "top-level" data structure and contains the plots as well
    as some other meta information (such as the style to be used). There may
    only be one ``graph`` per file.

    The ``graph`` roughly corresponds to matplotlib's ``figure`` class.

Plot
    A ``plot`` is a set of axes including the data plotted on those axes and any
    labels or annotations.

    A ``plot`` is similar to matplotlib's ``subplot``.

Axes
    ``axes`` contain the actual data to be plotted on the ``plot`` as well as
    legend titles for the data.

    The ``axes`` are equivalent to matplotlib's ``axes`` class.

From here on I will go into more depth on each of these data structures. Since
`Hip <https://github.com/mario-deluna/Hip>`_ is the unofficial "official" file
format of uniplot I will be giving examples in a Hip-like format but in the
interest of inclusion I will also be rewriting the examples in JSON.

.. note::

   Many strings can be given LaTeX style maths which will be typeset according
   to the `instructions <http://matplotlib.org/users/mathtext.html>`_ given by
   matplotlib. This largely applies to ``title``\ s, ``labels`` and
   ``legend``\ s.


.. _graph:

-----
Graph
-----

The graph is the top-level data structure. There can only be one graph per file
(which can be implied as we will see later) and each graph produces one file
when processed.

The attributes allowed in the graph are as follows (``title``, ``style`` and
``share`` are optional and default to an empty string, the standard style and
``yes`` respectively).

.. code-block:: yaml
   :caption: Graph attributes in Hip-like

   title: <string>
   style: <string>
   share: <bool>
   plots: <list: <object> | object>

.. code-block:: yaml
   :caption: A graph example in Hip

   title: "The Title of the Graph"
   style: "ggplot2"
   share: no
   plots: ...

.. code-block:: json
   :caption: A graph example in JSON

   {
       "title": "The Title of the Graph",
       "style": "ggplot2",
       "share": false,
       "plots": {}
   }

``title``
    This string will be placed centrally at the top of the graph. There is no
    default title. Titles may be given LaTeX style maths surrounded by ``$``.

``style``
    The graph will have this stylesheet applied to it if it can be found. If it
    is not specified (or the specified one can not be found) then the standard
    matplotlib style will be used.

``share``
    If the graph consists of multiple plots the values on the axes can be shared
    between the plots to make the graph less cluttered. This is on by default.

``plots``
    A list of plot objects or a single plot object. See :ref:`plot`.


.. _plot:

-----
Plots
-----

A plot sits within a graph. There can be as many plots as matplotlib can handle
(as far as I'm aware there is no specific cap on this) and all plots will be
placed on the graph in a roughly square shape.

The following attributes are allowed (``title`` and ``labels`` are optional).

.. code-block:: yaml
   :caption: Plot attributes in Hip-like

   title: <string>
   labels:
       x: <string>
       y: <string>
   axes: <list: <object>>

.. code-block:: yaml
   :caption: A plot example in Hip

   title: "The Title of This Particular Plot"
   labels:
       x: "The x-axis"
       y: "The y-axis"
   axes: ...

.. code-block:: json
   :caption: A plot example in JSON

   {
       "title": "The Title of This Particular Plot",
       "labels": {
           "x": "The x-axis",
           "y": "The y-axis"
       },
       "axes": {}
   }

``title``
    This string will be placed centrally above the plot. There is no default
    title. Titles may be given LaTeX style maths surrounded by ``$``.

``labels``
    These are the axis labels which will be placed next to the corresponding
    axis. These default to ``"x"`` and ``"y"`` and may be supplied LaTeX style
    maths.

.. todo:: Allow a single axes object as well as a list.

``axes``
    A list of axes objects. See :ref:`axes`.


.. _axes:

----
Axes
----

The axes contain the things which directly relate to each set of data. This is
easily the most complex part of the uniplot data structure since the data can be
specified in many ways.

In the first code-block below ``x`` and ``y`` have been specified twice to show
the composition of the object format. In the second and third blocks an array of
axes has been shown, to show the many ways of specifying an axis.

.. code-block:: yaml
   :caption: Axes attributes in Hip-like

   legend: <string>
   x: <list: <number> | string>
   x:
       values: <list: <number> | string>
       errors: <number | list: <number> | string>
   y: <list: <number> | string>
   y:
       values: <list: <number> | string>
       errors: <number | list: <number> | string>

.. code-block:: yaml
   :caption: Some axes examples in Hip

   -
   # 1
   legend: "A straight line."
   x: 0, 1, 2, 3, 4
   y: 0, 2, 4, 6, 8
   --
   # 2
   legend: "A quadratic."
   x:
       values: 0, 1, 2, 3
   y:
       values: 0, 1, 4, 9
   --
   # 3
   legend: "Noisy data."
   x:
       values: 1e6, 2e6, 3e6, 4e6, 5e6, 7e6
       errors: 0.01
   y:
       values: 2e-3, 4e-3, 5e-3, 9e-3, 8e-3, 12e-3
       errors: 1e-3, 1e-3, 1e-3, 2e-3, 3e-3, 1e-3
   --
   # 4
   legend: "Values obtained from a csv."
   x: "path/to/file.csv:0"
   y: "path/to/file.csv:1"
   --
   # 5
   legend: "Values obtained from a whitespace delimited file."
   x:
       values: "path/to/a/file.ext:0:1"
       errors: "path/to/a/file.ext:2:1"
   y:
       values: "path/to/a/file.ext:1:1"
       errors: "path/to/a/file.ext:3:1"
   --
   # 6
   x:
       values: 1, 2, 8, 5, 3, 5
       errors: "path/to/this/file.csv:0:2"
   y:
       values: "path/to/that/file.dat:4"
       errors: 0.3
   -

.. code-block:: json
   :caption: Some axes examples in JSON

   [
     {
       "legend": "A straight line.",
       "x": [0, 1, 2, 3, 4],
       "y": [0, 2, 4, 6, 8]
     },
     {
       "legend": "A quadratic.",
       "x": {"values": [0, 1, 2, 3]},
       "y": {"values": [0, 1, 4, 9]}
     },
     {
       "legend": "Noisy data.",
       "x": {
         "values": [1000000, 2000000, 3000000, 4000000, 5000000, 7000000],
         "errors": 0.01
       },
       "y": {
         "values": [0.002, 0.004, 0.005, 0.009, 0.008, 0.012],
         "errors": [0.001, 0.001, 0.001, 0.002, 0.003, 0.001]
       }
     },
     {
       "legend": "Values obtained from a csv.",
       "x": "path/to/file.csv:0",
       "y": "path/to/file.csv:1"
     },
     {
       "legend": "Values obtained from a whitespace delimited file.",
       "x": {
         "values": "path/to/a/file.ext:0:1",
         "errors": "path/to/a/file.ext:2:1"
       },
       "y": {
         "values": "path/to/a/file.ext:1:1",
         "errors": "path/to/a/file.ext:3:1"
       }
     },
     {
       "x": {
         "values": [1, 2, 8, 5, 3, 5],
         "errors": "path/to/this/file.csv:0:2"
       },
       "y": {
         "values": "path/to/that/file.dat:4",
         "errors": 0.3
       }
     }
   ]

``legend``
    The ``legend`` attribute gives the string to be used in the legend for that
    plot. If no ``axes`` has a ``legend`` attribute then the plot will not have
    a legend. There is no default legend label and LaTeX style maths can be used
    with legends.

``x`` and ``y``
    These contain the data to be plotted. If there is an ``errors`` supplied
    then an errorbar graph will be plotted, else a line graph will be plotted.

    The ``axes`` in the Hip example are numbered using comments, each ``axes``
    instance will  be explained in the following list (matching the numbers).

    #. This ``axes`` specifies both the x- and y-axis as a simple list of
       numbers. This will plot a line graph.

    #. This ``axes`` only uses a ``values`` attribute and plots a line graph.
       This works but is entirely redundant.

    #. This ``axes`` uses ``values`` and ``errors`` and therefore plots an
       errorbar graph. The x-axis gives ``errors`` as a single number, this
       number is considered a percentage error and is multiplied by each number
       in ``values`` to give the absolute error on that number. The y-axis is
       given as a list of numbers, these numbers are considered absolute errors.
       ``errors`` must either be a single number or it must be the same length
       as ``values``.

    #. This ``axes`` uses data from a CSV file (see :ref:`datafile`). The
       x-values are stored in the 0\ :superscript:`th` column and the y-values
       are stored in the 1\ :superscript:`st` column. These files do not have to
       be the same and do not need to be in consecutive columns.

    #. This ``axes`` stores both ``values`` and ``errors`` in a whitespace
       delimited file. The columns are in the order ``x-val|y-val|x-err|y-err``
       and one row must be skipped from each column.

    #. This ``axes`` shows that all the previous examples can be mixed and
       matched to your liking.


.. _datafile:

^^^^^^^^^^^^^^^^^^^^^^
Storing Data in a File
^^^^^^^^^^^^^^^^^^^^^^

.. todo::

   Allow data to be read from other filetypes such as ``.xls`` files and maybe
   even database files.

uniplot allows you to store ``values`` and ``errors`` in a file, this is useful
if you have a large amount of data which would be annoying and error prone to
write by hand. Currently only CSV and whitespaces delimited files are supported,
any file which does not have the extension :file:`.csv` is assumed to be a
whitespace delimited file.

To do this you must provide in the following format::

    "<path to file>:<zero-indexed column number>:<number of rows to skip>"

The path to the file can be either be relative to the directory from which the
program is run or it can be absolute. The zero-indexed column number is...
well... the column number of the data, zero-indexed. The number of rows to skip
is passed directly on to the ``skiprows`` argument of `numpy.loadtxt`_ and is
very useful if your file has header rows. The number of rows to skip does not
need to be specified and defaults to 0.

.. _numpy.loadtxt: http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html

-------------------
Omitting Structures
-------------------

You don't have to specify the graph in every file you write, since all
attributes (with the exception of ``plots``) in a graph are optional you can
omit them entirely. This mean you can turn the following:

.. code-block:: yaml

   plots:
       title: "Some title"
       labels:
           x: "x axis"
           y: "y axis"
       axes: ...

into this:

.. code-block:: yaml

   title: "Some title"
   label:
       x: "x axis"
       y: "y axis"
   axes: ...

Further still, all attributes of a plot are optional as well so you can omit
this too. So the following:

.. code-block:: yaml

   plots:
       axes:
           legend: "Legendary legend entry"
           x: 0, 1, 2, 3, 4
           y: 0, 2, 4, 6, 8

becomes:

.. code-block:: yaml

   legend: "Legendary legend entry"
   x: 0, 1, 2, 3, 4
   y: 0, 2, 4, 6, 8

See `examples`_ for more in-depth examples.
