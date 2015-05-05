=======
uniplot
=======

uniplot is simple utility which aims to unify plotting. The issue with modern
plotting programs such as EasyPlot and Origin (apart from the fact you have to
pay for them D:) is that they all use a different format to represent their
plots, meaning you have to have all the programs installed on your computer to
use these plots (an even bigger issue since these plots never seem to be
exportable to images).

uniplot is written in Python meaning it's cross-platform and easy to install.
uniplot uses a simple, human-readable data serialisation format called `Hip`_
and was designed so that users can modify (or even write from scratch) the file
themselves.

.. _`Hip`: https://github.com/mario-deluna/Hip

------------
Installation
------------

uniplot is currently not available on PyPI but installation is still as simple
as cloning the `repo`_ and using ``pip``::

    $ git clone https://github.com/Sean1708/uniplot.git
    $ pip install .

.. _`repo`: https://github.com/Sean1708/uniplot

---------------
The File Format
---------------

uniplot uses `Hip`_ data serialisation (interfaced using the `HipPy`_) to store
the data for the plot. The file stores a list of objects with the following
fields::

    -
    title: <string>
    labels:
        x: <string>
        y: <string>
    data: <string>
    data:
        -
        x:
            percent: <bool>
            values: <list: <int | float>>
            errors: <list: <int | float> | int | float>
        y:
            percent: <bool>
            values: <list: <int | float>>
            errors: <list: <int | float> | int | float>
        --
        ...
        -
    --
    ...
    -

.. _`HipPy`: https://github.com/Sean1708/HipPy
