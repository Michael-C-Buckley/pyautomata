# PyAutomata Rendering Module

# Python Modules
from typing import TYPE_CHECKING

# Third-Party Modules
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numpy import arange, random

# Local Modules
from pyautomata.stats import StatsContainer
if TYPE_CHECKING:
    from pyautomata.classes.canvas import Canvas

def prepare_plot(x_label: str, y_label: str, title: str, grid: bool = True,
                 legend: bool = False):
    """
    Wrapper function for de-cluttering common pyplot items
    """
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(grid)
    if legend:
        plt.legend()
    plt.show()

def prepare_scatter_plot(x: list, y: list):
    """
    Wrapper function for de-cluttering scatter plot creation
    """
    plt.style.use('_mpl-gallery')

    # size and color:
    random.seed(3)
    sizes = random.uniform(15, 80, len(x))
    colors = random.uniform(15, 80, len(x))

    # plot
    fig, ax = plt.subplots()

    ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

    ax.set(xlim=(0, 50), xticks=arange(1, 8),
        ylim=(0, 50), yticks=arange(1, 8))

    plt.show()

def prepare_bar_chart(inputs: list):
    """
    Wrapper function for de-cluttering bar chart creation
    """
    fig, ax = plt.subplots()

    x = 0.5 + arange(len(inputs))

    ax.bar(x, inputs, width=1, edgecolor="white", linewidth=0.7)

    ax.set(xlim=(0, 10), xticks=arange(1, len(inputs)),
           ylim=(0, 8), yticks=arange(1, len(inputs)))
    
    plt.show()


def draw_plot(canvas: 'Canvas', max_depth: int = None, filename: str = None,
              title: str = None):
    """
    Draw a canvas plot
    """
    if max_depth is None:
        max_depth = canvas.rows+1

    if title is None:
        title = f'Rule {canvas.rule}: {canvas.description}'

    inverted_cmap = LinearSegmentedColormap.from_list('inverted_gray', ['white', 'black'])

    plt.imshow(canvas.result[:, 1:max_depth*2], cmap=inverted_cmap)
    plt.title(title)
    
    if plt.isinteractive():
        plt.show()
    else:
        if filename is None:
            filename = title
        plt.savefig(filename)

def draw_standard_deviation(stats: StatsContainer, start: int = None, end: int = None) -> None:
    """
    Draw the standard deviations plots
    """
    plt.title('Row sum increase rate')
    start = start if start else 0
    end = end if end else len(stats.marginal_sum_increase)-1
    plot_values = [stats.marginal_sum_increase[i] for i in range(start, end+1)]
    plt.plot(plot_values)

    color_iterator = iter(['red', 'purple', 'orange', 'blue'])
    next_color = lambda: next(color_iterator, None)

    for i in range(4):
        color = next_color()
        get_value = lambda v: stats.increase_standard_deviations_map.get(v, None)
        for value in [get_value(i), get_value(-i)]:
            if value:
                plt.axhline(y=value, color=color)

    plt.grid()
    plt.show()
