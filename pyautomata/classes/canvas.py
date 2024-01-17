# Project PyAutomata Canvas Class Library

# Local Modules
from pyautomata.classes.basecanvas import BaseCanvas
from pyautomata.classes.general import Pattern
from pyautomata.render import draw_plot, draw_standard_deviation
from pyautomata.stats import StatsContainer, calculate_stats

class Canvas(BaseCanvas):
    """
    Intermediate class for methods that the Base class cannot to prevent
    circular import and dependency errors
    """
    def __init__(self, rule: int, rows: int = 100, pattern: Pattern = Pattern.STANDARD,
                 force_python: bool = False, generate: bool = True) -> None:
        super().__init__(rule, rows, pattern, force_python, generate)
        
        if generate:
            self._stats: StatsContainer = calculate_stats(self)

    @property
    def stats(self):
        if self.result is None:
            self.generate(self.pattern)
        if self._stats is None:
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

    def draw_sums_deviations(self, start: int = None, end: int = None):
        """
        Charts the calculated row sums and the standard deviations
        """
        draw_standard_deviation(self.stats, start, end)
    