# PyAutomata Base Canvas

# Python Modules
from enum import Enum
from os import path
from pickle import dump, load
from random import randint
from typing import TYPE_CHECKING

# Third-Party Modules
from appdirs import user_data_dir
from numpy import arange, zeros

# Local Modules
from pyautomata.classes.general import Pattern

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

    def __repr__(self) -> str:
        return f'Canvas: Rule {self.automata.rule} - {self.description}'

    def generate(self, pattern: Pattern = Pattern.STANDARD):
        """
        Generate the canvas based on the supplied pattern
        """
        rows = (self.columns//2) + 1
        canvas = zeros([rows, self.columns+2])

        # Pattern logic
        if pattern is Pattern.STANDARD:
            canvas[0, int(self.columns/2)+1] = 1
            row_sum = 1

        elif pattern is Pattern.RANDOM:
            row_sum = 0
            for i, _ in enumerate(canvas[0]):
                canvas[0][i] = randint(0, 1)
                row_sum = row_sum + canvas[0][i]
        
        elif pattern is Pattern.ALTERNATING:
            row_sum = 0
            for i, _ in enumerate(canvas[0]):
                if i % 2 == 0:
                    canvas[0][i] = 0
                else:
                    canvas[0][i] = 1
                    row_sum += 1
        
        self.sums = [row_sum]

        for i in arange(0, rows-1):
            self.sums.append(0)
            for j in arange(0, self.columns):
                local_pattern = tuple(canvas[i, j:j+3])
                output_pattern = self.automata.pattern.get(local_pattern)
                canvas[i+1, j+1] = output_pattern
                self.sums[i+1] += output_pattern

        self.result = canvas


    def save(self):
        """
        Method to save the canvas to avoid re-calculation in the future
        """
        filename = f'R{self.automata.rule} L{self.columns} {self.description}'
        file_path = path.join(CACHE_DIR, f'{filename}.pkl')
        
        with open(file_path, 'wb') as canvas_pickle:
            dump(self, canvas_pickle)