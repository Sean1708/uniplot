"""Handles the actual plotting of the file."""
import math
import numpy
import os.path
import warnings
import matplotlib
from matplotlib import pyplot


_LIST = (list, numpy.ndarray)


# TODO: should these have .plot(fig) methods?
class Graph:

    """The top level data structure, one file is one Graph."""

    def __init__(self, data):
        """Extract graph attributes."""
        if 'plots' in data:
            plots = data['plots']
            self.title = data.get('title', '')
            self.share = data.get('share', True)
            self.style = data.get('style')
        else:  # top-level object is a (list of) plot(s)
            plots = data
            self.title = ''
            # a single plot can't share with itself
            self.share = False
            self.style = None


        if isinstance(plots, _LIST):
            self.plots = [Plot(p) for p in plots]
        else:
            self.plots = [Plot(plots)]


class Plot:

    """One or more Plots sit within a Graph."""

    def __init__(self, data):
        """Extract plot attributes."""
        self.title = data.get('title', '')
        self.labels = data.get('labels', {'x': 'x', 'y': 'y'})
        axes = data['axes']

        if isinstance(axes, _LIST):
            self.axes = [Axes(a) for a in axes]
        else:
            self.axes = [Axes(axes)]


class Axes:

    """Axes contain the data to be plotted."""

    def __init__(self, data):
        """Extract axes attributes and data."""
        self.label = data.get('legend', '')
        get_axis_values(data, 'x', self.__dict__)
        get_axis_values(data, 'y', self.__dict__)


def round_half_up(n):
    """Round n, settling ties by rounding up.

    Python's default is to use banker's rounding and I can't find a way to
    override that so here we are.

    Works on negative numbers.
    """
    fl = math.floor(n)
    if n-fl < 0.5:
        return fl
    else:
        return fl+1


def get_axis_values(data, axis, args):
    """Extract the correct values from an axis."""
    # TODO: this is reallyreallyreally ugly
    if isinstance(data[axis], _LIST):  # hard-coded data
        args[axis] = numpy.array(data[axis])
    elif isinstance(data[axis], str):  # data in 'filename:column:skiprows'
        args[axis] = load_array_from_file(data[axis])
    else:  # data given with `values` and `errors`
        if isinstance(data[axis]['values'], str):
            args[axis] = load_array_from_file(data[axis]['values'])
        else:
            args[axis] = numpy.array(data[axis]['values'])

        if 'errors' in data[axis]:
            err_axis = axis + 'err'
            errors = data[axis]['errors']

            if isinstance(errors, _LIST):  # an error for each value
                args[err_axis] = numpy.array(errors)
            elif isinstance(errors, str):  # errors in file
                args[err_axis] = load_array_from_file(errors)
            else:  # error given as percentage
                args[err_axis] = args[axis] * errors


def load_array_from_file(file_info_str):
    """Load an array from a file."""
    file_info = file_info_str.split(':')
    delim = ',' if os.path.splitext(file_info[0])[1] == '.csv' else None
    return numpy.loadtxt(
        file_info[0], delimiter=delim, usecols=[int(file_info[1])],
        skiprows=0 if len(file_info) < 3 else int(file_info[2])
    )


def subplots(fig, nrows, ncols, nsubs, share):
    """Create a list of axes with correct ticks set to visible.

    Mirrors matplotlib.pyplot.subplots, though not exactly, so see the source
    code for tips.
    """
    axes = []
    for i in range(nsubs):
        # add_subplot is 1-indexed
        i += 1
        axis = fig.add_subplot(nrows, ncols, i)
        axes.append(axis)

        # true if there are plots below this one (visually)
        if share and i + ncols <= nsubs:
            for l in axis.get_xticklabels():
                l.set_visible(False)

        # true if not the first column
        if share and i % ncols != 1:
            for l in axis.get_yticklabels():
                l.set_visible(False)

    return axes


def plotwidth(figure, nrows, ncols):
    """Calculate the plot width of the figure, assuming square subplots.

    Does this by calculating the height per plot and multiplying by number of
    columns.
    """
    height = figure.get_figheight() / nrows
    return height * ncols


def plot_axis(canvas, data):
    """Correctly plot a set of x-y values."""
    # TODO: when this is refactored we can call vars() on the Axes object to
    # get the args.
    args = vars(data)

    if 'xerr' in args or 'yerr' in args:
        canvas.errorbar(fmt='o', **args)
    else:
        # plot doesn't support plot(x=..., y=...)
        canvas.plot(args.pop('x'), args.pop('y'), **args)


def plot_subplot(canvas, data):
    """Plot each subplot."""
    canvas.set_title(data.title)

    canvas.set_xlabel(data.labels['x'])
    canvas.set_ylabel(data.labels['y'])

    has_legend = False
    for axis in data.axes:
        if 'label' in axis.__dict__ and axis.label != '':
            has_legend = True
        plot_axis(canvas, axis)

    if has_legend:
        # TODO: don't bother with 'has_legend',
        # just temporarily suppress warnings
        canvas.legend(loc='best')


def plot_graph(data, filename):
    """Plot the data."""
    fig = pyplot.figure()
    fig.suptitle(data.title)

    nsubs = len(data.plots)
    # as close an approximation to square as possible without empty rows
    nrows = round_half_up(math.sqrt(nsubs))
    ncols = math.ceil(nsubs/nrows)

    axes = subplots(fig, nrows, ncols, nsubs, data.share)

    for (axis, plot) in zip(axes, data.plots):
        plot_subplot(axis, plot)

    # TODO: this is ok for mulit plots but horrible for single
    #fig.set_figwidth(plotwidth(fig, nrows, ncols))
    fig.savefig(filename)


def plot(data, filename):
    """Set the correct style then plot the data."""
    style_dir = os.path.join(os.path.expanduser('~'), '.uniplot', 'style')
    user_styles = os.listdir(style_dir)

    # TODO: just put data.style everywhere
    stylesheet = data.style

    # TODO: use plugin for styles (store them as dict then use rc=...)
    if stylesheet in user_styles:
        with matplotlib.rc_context(fname=os.path.join(style_dir, stylesheet)):
            plot_graph(data, filename)
    elif stylesheet in pyplot.style.available:
        with pyplot.style.context(stylesheet):
            plot_graph(data, filename)
    else:
        if stylesheet is not None:
            m = "style '{}' not found, using default.".format(stylesheet)
            warnings.warn(m)
        plot_graph(data, filename)
