# PyAutomata Rendering Module

# Python Modules
from typing import TYPE_CHECKING

# Third-Party Modules
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Local Modules
if TYPE_CHECKING:
    from pyautomata.classes.canvas import Canvas

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