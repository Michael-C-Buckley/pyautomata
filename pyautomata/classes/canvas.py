from typing import TYPE_CHECKING

from pyautomata.classes.basecanvas import BaseCanvas
from pyautomata.render import draw_plot, draw_standard_deviation
from pyautomata.stats import StatsContainer, calculate_stats

# Local Modules
from pyautomata.classes.general import Pattern

if TYPE_CHECKING:
    from pyautomata.classes.automata import Automata

class Canvas(BaseCanvas):
    """
    Intermediate class for methods that the Base class cannot to prevent
    circular import and dependency errors
    """
    def __init__(self, automata: 'Automata', pattern: Pattern = Pattern.STANDARD,
                 columns: int = 100, force_python: bool = False,
                 generate: bool = True) -> None:
        super().__init__(automata, pattern, columns, force_python, generate)
        
        if generate:
            self._stats: StatsContainer = calculate_stats(self)

    @property
    def stats(self):
        if not self.result:
            self.generate(self.pattern)
        if not self._stats:
            self._stats: StatsContainer = calculate_stats(self)
        return self._stats

    def render(self, max_depth: int = None, filename: str = None):
        """
        Draws a visual representation of the canvas
        """
        if max_depth is not None:
            if max_depth < self.columns:
                raise ValueError(f'Max depth cannot exceed canvas columns ({max_depth} v. {self.columns})')
        draw_plot(self, max_depth, filename)

    def draw_sums_deviations(self):
        """
        Charts the calculated row sums and the standard deviations
        """
        draw_standard_deviation(self.stats, self)