"""Handles the actual plotting of the file."""
import math
import numpy
import os.path
import warnings
import matplotlib
from matplotlib import pyplot


_LIST = (list, numpy.ndarray)


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

    def plot(self, canvas):
        """Set attributes for the entire graph."""
        nsubs = len(self.plots)
        # as close an approximation to square as possible without empty rows
        nrows = round_half_up(math.sqrt(nsubs))
        ncols = math.ceil(nsubs/nrows)

        # TODO: should this be a method?
        mpl_axes = subplots(canvas, nrows, ncols, nsubs, self.share)

        for (mpl_axis, subplot) in zip(mpl_axes, self.plots):
            subplot.plot(mpl_axis)


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

    def plot(self, canvas):
        """Set the attributes for each plot within the graph."""
        canvas.set_title(self.title)

        canvas.set_xlabel(self.labels['x'])
        canvas.set_ylabel(self.labels['y'])

        for axis in self.axes:
            axis.plot(canvas)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            canvas.legend(loc='best')


class Axes:

    """Axes contain the data to be plotted."""

    def __init__(self, data):
        """Extract axes attributes and data."""
        self.label = data.get('legend', '')
        self.parse_axis_values(data, 'x')
        self.parse_axis_values(data, 'y')

    def plot(self, canvas):
        """Plot data onto the axis."""
        # attributes of Axes corresponds to the function arguments
        args = vars(self)

        if 'xerr' in args or 'yerr' in args:
            canvas.errorbar(fmt='o', **args)
        else:
            # plot doesn't support plot(x=..., y=...)
            canvas.plot(args.pop('x'), args.pop('y'), **args)

    def parse_axis_values(self, data, axis):
        """Extract values of axis data."""
        # TODO: this is reallyreallyreally ugly, split it into multiple methods
        if isinstance(data[axis], _LIST):  # hard-coded data
            self.__dict__[axis] = numpy.array(data[axis])
        elif isinstance(data[axis], str):  # data in 'filename:column:skiprows'
            self.__dict__[axis] = load_array_from_file(data[axis])
        else:  # data given with `values` and `errors`
            if isinstance(data[axis]['values'], str):
                self.__dict__[axis] = load_array_from_file(
                    data[axis]['values']
                )
            else:
                self.__dict__[axis] = numpy.array(data[axis]['values'])

            if 'errors' in data[axis]:
                err_axis = axis + 'err'
                errors = data[axis]['errors']

                if isinstance(errors, _LIST):  # an error for each value
                    self.__dict__[err_axis] = numpy.array(errors)
                elif isinstance(errors, str):  # errors in file
                    self.__dict__[err_axis] = load_array_from_file(errors)
                else:  # error given as percentage
                    self.__dict__[err_axis] = self.__dict__[axis] * errors


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


def load_array_from_file(file_info_str):
    """Load an array from a file.

    Stored as 'filename:column:skiprows'.
    """
    # TODO:
    #   make filename behave relative to .hip file unless an absolute string
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


# TODO: maybe use style as a property?
# TODO: maybe use as context manager to avoid the if statements
def plot_with_style(data, canvas):
    """Set the correct style then plot the data."""
    style_dir = os.path.join(os.path.expanduser('~'), '.uniplot', 'style')
    user_styles = os.listdir(style_dir)

    # TODO: use plugin for styles (store them as dict then use rc=...)
    # TODO: have a way to use default regardless of data.style
    if data.style in user_styles:
        with matplotlib.rc_context(fname=os.path.join(style_dir, data.style)):
            data.plot(canvas)
    elif data.style in pyplot.style.available:
        with pyplot.style.context(data.style):
            data.plot(canvas)
    else:
        if data.style is not None:
            m = "style '{}' not found, using default.".format(data.style)
            warnings.warn(m)
        data.plot(canvas)
