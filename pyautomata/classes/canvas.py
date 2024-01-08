from typing import TYPE_CHECKING

from pyautomata.classes.basecanvas import BaseCanvas
from pyautomata.render import draw_plot

if TYPE_CHECKING:
    from pyautomata.classes.automata import Automata

class Canvas(BaseCanvas):
    """
    Intermediate class for methods that the Base class cannot to prevent
    circular import and dependency errors
    """
    def __init__(self, automata: 'Automata', description: str = '', columns: int = 100) -> None:
        super().__init__(automata, description, columns)

    def render(self, max_depth: int = None, filename: str = None):
        if max_depth is not None:
            if max_depth < self.columns:
                raise ValueError(f'Max depth cannot exceed canvas columns ({max_depth} v. {self.columns})')
        draw_plot(self, max_depth, filename)