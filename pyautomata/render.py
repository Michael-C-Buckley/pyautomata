# PyAutomata Rendering Module

# Python Modules
from typing import TYPE_CHECKING

# Third-Party Modules
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from numpy import array, ndarray, float32

# Local Modules
from pyautomata.stats import StatsContainer
if TYPE_CHECKING:
    from pyautomata.classes.canvas import Canvas

def yEq(value: float, length: int) -> ndarray:
    """
    Returns a line space that is a flat line of specified length
    """
    yFunc = []
    for i in range(length):
        yFunc.append(value)

    return array(yFunc, float32)

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

def draw_standard_deviation(stats: StatsContainer, canvas: 'Canvas'):
    """
    Draw the standard deviations plots
    """
    plt.title('Row sum average rate')
    plt.plot(stats.sum_rate_average)

    color_iterator = iter(['red', 'purple', 'orange', 'blue'])
    next_color = lambda: next(color_iterator, None)

    for i in range(4):
        color = next_color()
        get_value = lambda v: stats.standard_deviations_map.get(v, None)
        for value in [get_value(i), get_value(-i)]:
            plt.plot(yEq(value , (canvas.columns)//2), color=color)

    plt.grid()
    plt.show()