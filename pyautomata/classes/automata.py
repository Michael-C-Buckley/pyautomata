# Cellular Automata

# Python Modules
from pickle import dump, load
from os import path

# Third-Party Modules
from appdirs import user_data_dir
from numpy import binary_repr

# Local Modules
from pyautomata.classes.canvas import Canvas

CACHE_DIR = user_data_dir()


class Automata:
    def __init__(self, rule: int) -> None:
        # Validation
        init_except_message = 'Rule must be an integer between 1 and 256'
        if type(rule) != int:
            raise ValueError(init_except_message)
        if not 1 <= rule <= 256:
            raise ValueError(init_except_message)
        
        pattern = {}
        output_pattern = [int(x) for x in binary_repr(rule, width=8)]

        for i in range(8):
            input_pattern = tuple([int(x) for x in binary_repr(7-i, 3)])
            pattern[input_pattern] = output_pattern[i]

        self.rule = rule
        self.pattern = pattern

    def __repr__(self) -> str:
        return f'Automata: Rule {self.rule}'
    
    def get_canvas(self, columns: int = 100) -> 'Canvas':
        """
        Method to generate the typical pattern, starting with a single point.

        `columns` is an `int` of the deep that the canvas will be generated to
        """
        description = 'Standard center start'
        filename = f'R{self.rule} L{columns} {description}'

        try:
            with open(path.join(CACHE_DIR, f'{filename}.pkl'), 'rb') as file:
                canvas = load(file)
        except Exception as e:
            canvas = Canvas(self, description, columns)

        return canvas
    
    def save_canvas(self, canvas: 'Canvas'):
        """
        Method to save a canvas
        """
        filename = f'R{self.rule} L{canvas.columns} {canvas.description}'
        file_path = path.join(CACHE_DIR, f'{filename}.pkl')
        
        with open(file_path, 'wb') as canvas_pickle:
            dump(canvas, canvas_pickle)
