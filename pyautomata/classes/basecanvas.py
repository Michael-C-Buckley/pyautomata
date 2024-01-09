# PyAutomata Base Canvas

# Python Modules
from enum import Enum
from os import path
from pickle import dump, load
from random import randint
from typing import TYPE_CHECKING

# Third-Party Modules
from appdirs import user_data_dir
from numpy import arange, zeros, ascontiguousarray, uint8

# Local Modules
from pyautomata.classes.general import Pattern
from pyautomata.handlers.rust import generate_canvas

if TYPE_CHECKING:
    from pyautomata.classes.automata import Automata

CACHE_DIR = user_data_dir()

class BaseCanvas:
    """
    Canvas base class containing fundamental attributes
    """
    def __init__(self, automata: 'Automata', pattern: Pattern = Pattern.STANDARD,
                 columns: int = 100) -> None:
        
        self.columns = columns
        self.automata = automata
        self.description = pattern.value

        self.generate(pattern)

        # self.result = generate_canvas()

    def __repr__(self) -> str:
        return f'Canvas: Rule {self.automata.rule} - {self.description}'

    def generate(self, pattern: Pattern = Pattern.STANDARD):
        """
        Generate the canvas based on the supplied pattern
        """
        rows = (self.columns//2) + 1
        canvas = zeros([rows, self.columns], uint8)
        ascontiguousarray(canvas)

        pattern_map = {
            Pattern.LEFT: 0,
            Pattern.RIGHT: self.columns,
            Pattern.STANDARD: self.columns//2,
        }
        patter_iteration_map = {
            Pattern.RANDOM: lambda _: randint(0, 1),
            Pattern.ALTERNATING: lambda i: 0 if i % 2 == 0 else 1,
        }

        row_sum = 0

        # Pattern logic
        if pattern in pattern_map:
            canvas[0, pattern_map[pattern]] = 1
            row_sum = 1

        if pattern in patter_iteration_map:
            func = patter_iteration_map[pattern]
            for i, _ in enumerate(canvas[0]):
                value = func(i)
                canvas[0][i] = value
                row_sum += value

        self.sums = [row_sum]

        canvas = generate_canvas(canvas[0], rows, self.columns, self.automata.flat_pattern)

        self.result = canvas

    def save(self):
        """
        Method to save the canvas to avoid re-calculation in the future
        """
        filename = f'R{self.automata.rule} L{self.columns} {self.description}'
        file_path = path.join(CACHE_DIR, f'{filename}.pkl')
        
        with open(file_path, 'wb') as canvas_pickle:
            dump(self, canvas_pickle)