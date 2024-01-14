# PyAutomata Base Canvas

# Python Modules
from os import path
from pickle import dump
from random import randint
from typing import TYPE_CHECKING

# Third-Party Modules
from numpy import (
    arange, array, ascontiguousarray, 
    save as np_save, load as np_load, insert as np_insert,
    zeros, uint8, ndarray,
)

# Local Modules
from pyautomata.classes.general import Pattern
from pyautomata.handlers import generate_canvas, RUST_AVAILABLE
from pyautomata.version import VERSION

if TYPE_CHECKING:
    from pyautomata.classes.automata import Automata

class BaseCanvas:
    """
    Canvas base class containing fundamental attributes
    """
    def __init__(self, automata: 'Automata', pattern: Pattern = Pattern.STANDARD,
                 columns: int = 100, force_python: bool = False,
                 generate: bool = True) -> None:
        
        pattern = pattern if isinstance(pattern, Pattern) else Pattern.from_string(pattern)
        
        self.columns = columns
        self.automata = automata
        self.description = pattern.value
        self.version = VERSION
        self.pattern = pattern
        self.sums = None
        self.result = None

        if generate:
            self.generate(pattern, force_python=force_python)

    def __repr__(self) -> str:
        return f'Canvas: Rule {self.automata.rule} - {self.description}'

    def generate(self, pattern: Pattern = Pattern.STANDARD,
                 force_python: bool = False):
        """
        Procedure to generate the canvas based on the supplied pattern.
        `force_python` will bypass the Rust API and use Python native logic.
        """
        if pattern in [Pattern.RIGHT, Pattern.LEFT]:
            rows = self.columns
        else:
            rows = (self.columns//2)
        canvas = zeros([rows, self.columns], uint8)
        ascontiguousarray(canvas)

        pattern_map = {
            Pattern.LEFT: 0,
            Pattern.RIGHT: self.columns-1,
            Pattern.STANDARD: self.columns//2,
        }
        pattern_iteration_map = {
            Pattern.RANDOM: lambda _: randint(0, 1),
            Pattern.ALTERNATING: lambda i: 0 if i % 2 == 0 else 1,
        }

        row_sum = 0

        # Interim value
        self.sums = [row_sum]

        # Pattern logic
        if pattern in pattern_map:
            canvas[0, pattern_map[pattern]] = 1
            row_sum = 1

        if pattern in pattern_iteration_map:
            func = pattern_iteration_map[pattern]
            for i, _ in enumerate(canvas[0]):
                value = func(i)
                canvas[0][i] = value
                row_sum += value

        boost = True if pattern in pattern_map else False
        central_line = 0 if not boost else pattern_map[pattern]

        if RUST_AVAILABLE and not force_python:
            canvas, sums = generate_canvas(canvas[0], rows, self.columns, self.automata.flat_pattern, boost, central_line)
            self.sums = np_insert(sums, 0, row_sum)
        else:
            canvas = self.python_generate(canvas, rows, boost, central_line)

        self.result = canvas


    def python_generate(self, canvas: ndarray, rows: int, boost: bool = False, central_line: int = 0):
        """
        Alternative function to internally generate a canvas instead of using
        the Rust API
        """

        for i in arange(0, rows-1):

            # Boost masking area determination
            start = (central_line - i - 1) if boost else 0
            stop = min((central_line + i + 1, self.columns-1)) if boost else self.columns-1

            self.sums.append(0)
            for j in arange(start, stop):
                local_pattern = tuple(canvas[i, j:j+3])
                output_pattern = self.automata.pattern.get(local_pattern, 0)
                canvas[i+1, j+1] = output_pattern
                self.sums[i+1] += output_pattern

        self.sums = array(self.sums)

        return canvas
