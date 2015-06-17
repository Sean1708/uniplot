"""Handles the actual plotting of the file."""
import math
import numpy
import os.path
import matplotlib.pyplot as plt


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
    height = figure.get_figheight()/nrows
    return height * ncols


def plot(data, filename):
    """Plot the data."""
    fig = plt.figure()
    if 'graphs' in data:
        graphs = data['graphs']
        share = data.get('share', True)
        if 'title' in data:
            fig.suptitle(data['title'])
    else:  # top-level object is the graph
        graphs = data
        # a single graph can't share it's own axis
        share = False

    if not isinstance(graphs, list):
        graphs = [graphs]
    nsubs = len(graphs)

    # as close an approximation to square as possible without empty rows
    nrows = round_half_up(math.sqrt(nsubs))
    ncols = math.ceil(nsubs/nrows)

    axes = subplots(fig, nrows, ncols, nsubs, share)

    for (axis, graph) in zip(axes, graphs):
        plot_subplot(axis, graph)

    fig.set_figwidth(plotwidth(fig, nrows, ncols))
    fig.savefig(filename)


def plot_subplot(canvas, data):
    """Plot each subplot."""
    title = data.get('title')
    if title is not None:
        canvas.set_title(title)

    labels = data.get('labels', {'x': 'x', 'y': 'y'})
    canvas.set_xlabel(labels['x'])
    canvas.set_ylabel(labels['y'])

    has_legend = False
    for axis in data['axes']:
        if 'legend' in axis:
            has_legend = True
        plot_axis(canvas, axis)

    if has_legend:
        canvas.legend()


def plot_axis(canvas, data):
    """Correctly plot a set of x-y values."""
    args = {}

    get_axis_values(data, 'x', args)
    get_axis_values(data, 'y', args)

    if 'legend' in data:
        args['label'] = data['legend']

    if 'xerr' in args or 'yerr' in args:
        canvas.errorbar(fmt='o', **args)
    else:
        # plot doesn't support plot(x=..., y=...)
        canvas.plot(args.pop('x'), args.pop('y'), **args)


def get_axis_values(data, axis, args):
    """Extract the correct values from an axis."""
    # TODO: this is reallyreallyreally ugly
    if isinstance(data[axis], list):  # hard-coded data
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

            if isinstance(errors, list):  # an error for each value
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
