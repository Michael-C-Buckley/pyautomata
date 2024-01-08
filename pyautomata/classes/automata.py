# Cellular Automata

# Python Modules
from pickle import load
from os import path

# Third-Party Modules
from appdirs import user_data_dir
from numpy import binary_repr

# Local Modules
from pyautomata.classes.canvas import Canvas
from pyautomata.classes.general import Pattern

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
    
    def get_canvas(self, pattern: Pattern = Pattern.STANDARD,
                   columns: int = 100, save: bool = True,
                   regenerate: bool = False) -> 'Canvas':
        """
        Method to generate the typical pattern, starting with a single point.

        `columns` is an `int` of the deep that the canvas will be generated to
        """
        filename = f'R{self.rule} L{columns} {pattern.value}'

        generate = lambda: Canvas(self, pattern, columns)

        if regenerate:
            canvas = generate()

        else:
            try:
                with open(path.join(CACHE_DIR, f'{filename}.pkl'), 'rb') as file:
                    return load(file)
            except Exception as e:
                canvas = generate()
        
        if save:
            canvas.save()

        return canvas