# PyAutomata Base Canvas

# Python Modules
from typing import TYPE_CHECKING

# Third-Party Modules
from numpy import arange, zeros

if TYPE_CHECKING:
    from pyautomata.classes.automata import Automata

class BaseCanvas:
    """
    Canvas base class containing fundamental attributes
    """
    def __init__(self, automata: 'Automata', description: str = '', columns: int = 100) -> None:
        self.columns = columns
        self.automata = automata
        self.description = description

        rows = (self.columns//2) + 1
        canvas = zeros([rows, self.columns+2])
        canvas[0, int(self.columns/2)+1] = 1
        self.sums = [1]

        for i in arange(0, rows-1):
            self.sums.append(0)
            for j in arange(0, self.columns):
                local_pattern = tuple(canvas[i, j:j+3])
                output_pattern = self.automata.pattern.get(local_pattern)
                canvas[i+1, j+1] = output_pattern
                self.sums[i+1] += output_pattern

        self.result = canvas

    def __repr__(self) -> str:
        return f'Canvas: Rule {self.automata.rule} - {self.description}'