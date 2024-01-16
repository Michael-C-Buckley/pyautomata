# PyAutomata Rendering Module

# Python Modules
from typing import TYPE_CHECKING, Any

# Third-Party Modules
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numpy import array, ndarray, float32

# Local Modules
from pyautomata.stats import StatsContainer
if TYPE_CHECKING:
    from pyautomata.classes.canvas import Canvas

def y_equals(value: float, length: int) -> ndarray:
    """
    Returns a line space that is a flat line of specified length
    """
    yFunc = []
    for i in range(length):
        yFunc.append(value)

    return array(yFunc, float32)

def prepare_plot(x_label: str, y_label: str, title: str, grid: bool = True,
                 legend: bool = False):
    """
    Wrapper function for de-cluttering common pyplot items
    """
    plt.xlabel(x_label)
    plt.ylabel(y_label);
    plt.title(title)
    plt.grid(grid)
    if legend:
        plt.legend()
    plt.show()

def draw_plot(canvas: 'Canvas', max_depth: int = None, filename: str = None):
    """
    Draw a canvas plot
    """
    if max_depth is None:
        max_depth = canvas.columns+1

    inverted_cmap = LinearSegmentedColormap.from_list('inverted_gray', ['white', 'black'])

    plt.imshow(canvas.result[:, 1:max_depth], cmap=inverted_cmap)
    title = f'Rule {canvas.automata.rule}: {canvas.description}'
    plt.title(title)
    
    if plt.isinteractive():
        plt.show()
    else:
        if filename is None:
            filename = title
        plt.savefig(filename)

def draw_standard_deviation(stats: StatsContainer, canvas: 'Canvas',
                            start: int = None, end: int = None) -> None:
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
            plt.plot(y_equals(value , end//2), color=color)

    plt.grid()
    plt.show()
