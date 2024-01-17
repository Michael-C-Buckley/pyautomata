# PyAutomata Base Canvas

# Python Modules
from random import randint

# Third-Party Modules
from numpy import (
    arange, array, ascontiguousarray, 
    insert as np_insert, binary_repr,
    zeros, uint8, ndarray,
)

# Local Modules
from pyautomata.classes.general import Pattern
from pyautomata.handlers.rust import generate_canvas, RUST_AVAILABLE
from pyautomata.version import VERSION

class BaseCanvas:
    """
    Canvas base class containing fundamental attributes
    """
    def __init__(self, rule: int, rows: int = 100, pattern: Pattern = Pattern.STANDARD,
                 force_python: bool = False, generate: bool = True) -> None:
        init_except_message = 'Rule must be an integer between 1 and 256'
        if type(rule) != int:
            raise ValueError(init_except_message)
        if not 1 <= rule <= 256:
            raise ValueError(init_except_message)
        
        pattern = pattern if isinstance(pattern, Pattern) else Pattern.from_string(pattern)
        
        self.rows = rows
        self.columns = self.rows if pattern in [Pattern.RIGHT, Pattern.LEFT] else (self.rows*2)

        self.rule = rule
        self.description = pattern.value

        self.version = VERSION
        self.pattern = pattern

        self.sums = None
        self.result = None

        # Generate the rule set that dictates generation behavior
        rule_set = {}
        flat_rule_set = []
        output_rule_set = [int(x) for x in binary_repr(rule, width=8)]

        for i in range(8):
            input_rule_set = tuple([int(x) for x in binary_repr(7-i, 3)])
            rule_set[input_rule_set] = output_rule_set[i]
            flat_rule_set.extend(input_rule_set)
            flat_rule_set.append(output_rule_set[i])

        self.rule = rule
        self.rule_set = rule_set
        self.flat_rule_set = array(flat_rule_set, uint8)

        if generate:
            self.generate(pattern, force_python)

    def __repr__(self) -> str:
        return f'Canvas: Rule {self.rule} - {self.description}'
    
    def generate(self, pattern: Pattern = Pattern.STANDARD,
                 force_python: bool = False):
        """
        Procedure to generate the canvas based on the supplied pattern.
        `force_python` will bypass the Rust API and use Python native logic.
        """
        canvas = zeros([self.rows, self.columns], uint8)
        ascontiguousarray(canvas)

        pattern_map = {
            Pattern.LEFT: 0,
            Pattern.RIGHT: self.rows-1,
            Pattern.STANDARD: self.columns//2,
        }
        pattern_iteration_map = {
            Pattern.RANDOM: lambda _: randint(0, 1),
            Pattern.ALTERNATING: lambda i: 0 if i % 2 == 0 else 1,
        }

        row_sum = 0

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

        self.sums = [row_sum]

        boost = True if pattern in pattern_map else False
        central_line = 0 if not boost else pattern_map[pattern]

        if RUST_AVAILABLE and not force_python:
            canvas, sums = generate_canvas(canvas[0], self.rows, self.columns, self.flat_rule_set, boost, central_line)
            self.sums = np_insert(sums, 0, row_sum)
        else:
            canvas = self.python_generate(canvas, self.rows, boost, central_line)

        self.result = canvas

    def python_generate_row(self, input_row: ndarray, start: int, stop: int) -> tuple[ndarray, int]:
        """
        Method to generate the next row given an input row
        """
        new_row = zeros((self.columns,), uint8)
        row_sum = 0
        
        for i in arange(start, stop):
            local_pattern = tuple(input_row[i:i+3])
            output_pattern = self.rule_set.get(local_pattern, 0)
            new_row[i+1] = output_pattern
            row_sum += output_pattern

        return new_row, row_sum


    def python_generate(self, canvas: ndarray, rows: int, boost: bool = False, central_line: int = 0):
        """
        Alternative function to internally generate a canvas instead of using
        the Rust API
        """
        for i in arange(0, rows-1):
            start = (central_line - i - 2) if boost else 0
            stop = min((central_line + i + 2, self.columns-1)) if boost else self.columns-1

            new_row, row_sum = self.python_generate_row(canvas[i], start, stop)
            self.sums.append(row_sum)
            canvas[i+1] = new_row

        self.sums = array(self.sums)

        return canvas
    