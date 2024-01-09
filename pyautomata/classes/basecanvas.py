# PyAutomata Base Canvas

# Python Modules
from os import path
from pickle import dump
from random import randint
from typing import TYPE_CHECKING

# Third-Party Modules
from appdirs import user_data_dir
from numpy import (
    arange, zeros, ascontiguousarray, 
    save as np_save, load as np_load,
    uint8, ndarray
)

# Local Modules
from pyautomata.classes.general import Pattern

# Foreign Function Interfacing and checking
RUST_AVAILABLE = False
try:
    from pyautomata.handlers.rust import generate_canvas
    RUST_AVAILABLE = True
except OSError:
    pass

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

        if RUST_AVAILABLE:
            canvas = generate_canvas(canvas[0], rows, self.columns, self.automata.flat_pattern)
        else:
            print('PyAutomata Warning: Rust binary not found, falling back on Python logic')
            canvas = self.python_generate(canvas, rows)

        self.result = canvas

    def python_generate(self, canvas: ndarray, rows: int):
        """
        Alternative function to internally generate a canvas instead of using
        the Rust API
        """

        for i in arange(0, rows-1):
            self.sums.append(0)
            for j in arange(0, self.columns-1):
                local_pattern = tuple(canvas[i, j:j+3])
                output_pattern = self.automata.pattern.get(local_pattern, 0)
                canvas[i+1, j+1] = output_pattern
                self.sums[i+1] += output_pattern

        return canvas
    
    def get_filename(self):
        """
        Returns the standard format for the filename for file caching minus extension
        """
        filename = f'R{self.automata.rule} L{self.columns} {self.description}'
        file_path = path.join(CACHE_DIR, filename)
        return file_path
        

    def save(self):
        """
        Method to save the canvas to avoid re-calculation in the future
        """
        filename = self.get_filename()

        # Separately save the array for performance reasons
        canvas_array = self.result
        self.save_array(f'{filename}.npy')
        self.result = None
        
        with open(f'{filename}.pkl', 'wb') as canvas_pickle:
            dump(self, canvas_pickle)

        # Put the array back for normal use
        self.result = canvas_array

    def save_array(self, filename: str = None):
        """
        Method to save the NumPy array for performance
        """
        filename = f'{self.get_filename()}.npy' if not filename else filename
        np_save(filename, self.result)

    def load_array(self, filename: str = None):
        """
        Method to load saved NumPy array
        """
        filename = f'{self.get_filename()}.npy' if not filename else filename
        array = np_load(filename)
        self.result = array
        return array
