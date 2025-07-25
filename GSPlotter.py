##############################################################################
import os
from pathlib import Path
import matplotlib.pyplot as plt


### GSPlotter ###
"""
This module is meant to imported in other programs.
It is a general use plotting software for usage in the GRBA group

Usage:
  With GSPlotter.py in the same folder (or with an absolute path)
  in your program, import GSPlotter as gsp

Call GSPlotter with gsp.plotter(data1, data2, ...)
  with the information you want to plot


Example plot creation:

gsp.plotter(
    x_data=[[1,2],[3,4],[5,6]],             # Data for the x-axis
    y_data=[[5,6],[3,4],[1,2]],             # Data for the y-axis
    xlabel='f(x) = 123',                    # Title on the bottom of the plot
    ylabel='f(y) = 456',                    # Title across the side of the plot
    title='plot_title',                     # Title on the top of the plot
    plot_labels=["str1", "str2", "str3"],   # For the legend
    filename='figure.png',                  # Figure file name
    colors=['red','gold','green'],          # Three random colors       *optional*
    line_styles=["-", "--", ":"],           # Three random linestyles   *optional*
    scale='linear'                          # How you view the data     *optional*
)
"""

# List of line colors for matplotlib
# This list will only be used if no other color list is passed
default_color_list = [
        "red",
        "gold",
        "limegreen",
        "dodgerblue",
        "purple",
        "darkorange",
        "teal",
        "mediumblue",
        "crimson",
        "forestgreen",
        "slategray",
        "magenta",
        "olive",
        "steelblue",
        "indianred"
]

# These line styles will be used unless some other set of
#   line styles is specified
default_line_styles = [
        "-",                # solid
        "--",               # dashed
        "-.",               # dash-dot
        ":",                # dotted
        (0, (1, 1)),        # densely dotted
        (0, (3, 1)),        # loosely dashed
        (0, (5, 2)),        # medium-long dash
        (0, (3, 5, 1, 5)),  # dash-dot with gaps
        (0, (5, 1)),        # tight dash
        (0, (1, 2, 3, 2)),  # complex pattern
    ]



def setup_plot(title, xlabel, ylabel, scale):
    """
    setup_plot()

    This function creates a base plot with no data.

    Parameters: All taken from plotter()
        title  - string -> top of the figure
        xlabel - string -> bottom of the figure
        ylabel - string -> left of the figure
        scale  - string -> linear or log view (other options exist)

    Output:
        Returns fig and ax
    """

    # Create a figure and a set of subplots.
    # This is the standard object-oriented way to make a plot.
    # figsize determines the shape of the figure, for more details
    #   about why these numbers are used, see comments above plt.savefig
    fig, ax = plt.subplots(figsize=(12, 6))

    # Use the ax object to set the labels of the plot.
    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)

    # Add a grid with lines that look like "--" that are 70% transparent
    plt.grid(True, linestyle="--", alpha=0.7)

    # Setting the scale of the plots to linear

    plt.xscale(scale)
    plt.yscale(scale)

    return fig, ax

# The strings in the arguments are default values if nothing else is passed
# They shouldn't be used, but it's nice to have to avoid weird errors
def plotter(x_values, y_values, plot_labels, title, scale='linear',
            xlabel="x-axis", ylabel="y-axis", filename='Default_Filename.png',
            colors=default_color_list, line_styles=default_line_styles):
    """
    plotter()

    This is a general plotting function.
    It takes in the data values, the labels, colors, and filename
    This function only takes the values for plotting, the plots are
        made in plotter()

    Parameters:
    # A list of lists with the values you want along the x-axis
    x_values

    # A list of lists with the values you want along the y-axis
    y_values

    # Names for each of your plots, same size as the outer list of x/y_values
    plot_labels

    # A *meaningful* name for the plot
    title

    # Label for the x-axis
    xlabel

    # Label for the y-axis
    ylabel

    # Color of the line(s)
    color

    # Name of the file you want the plot to be called
    filename

    Output:
    returns figure, which is to be passed into plotter()
    """

    # This creates a plots folder if it doesn't already exist
    plots_path = Path("plots")
    plots_path.mkdir(exist_ok=True)

    # Call the setup function to hold the plot objects
    # "log" is another option for scale
    fig, ax = setup_plot(title, xlabel, ylabel, scale=scale)

    # This is a nonfatal error check to avoid a silent error later
    # If the values aren't of uniform length, it won't plot the later lines
    if len(x_values) == len(y_values) == len(plot_labels):
        pass
    else:
        print(f"ERROR: The length of x_values, y_values, and plot_labels should be uniform. \n\
            \n length of x_values = {len(x_values)} \
            \n length of y_values = {len(y_values)} \
            \n length of plot_labels = {len(plot_labels)}"
            )


    # zip() allows us to iterate through multiple values at the same
    #   time to pass into ax.plot()
    for items in zip(x_values, y_values, plot_labels, colors, line_styles):

        # This chunk isn't necessary, but
        #   I think it makes sense conceptually to
        #   assign the values back to meaningful variable names
        x = items[0]
        y = items[1]
        label = items[2]
        color = items[3]
        line_style = items[4]

        # This is where the magic happens 😎😎😎
        # It will plot n lines on the graph
        #   where n is the amount of iterations
        #   for example, x_values = [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]
        #   would be n = 3 since there are 3 items in the outer list
        ax.plot(x, y, linestyle=line_style, color=color, label=label)

    # We want a legend, let's put it at the top right semi-arbitrarily
    # It's best to do this after plotting the data with labels
    ax.legend(loc="upper right")

    # Adjusts the padding a bit.
    # It also prevents labels from being cut out
    fig.tight_layout()

    # -- Plot Data -- #

    fig.savefig(os.path.join("./plots", filename), dpi=200)

    return


if __name__ == "__main__":
    print("Please see usage instructions at the top of GSPlotter.py")
    print("This program is not meant to be run, please import it")
    print("You can import this program with the following line of code:")
    print("import GSPlotter as gsp")