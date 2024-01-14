# Cellular Automata

# Third-Party Modules
from numpy import array, binary_repr, uint8

# Local Modules
from pyautomata.classes.canvas import Canvas
from pyautomata.classes.general import Pattern

class Automata:
    def __init__(self, rule: int) -> None:
        # Validation
        init_except_message = 'Rule must be an integer between 1 and 256'
        if type(rule) != int:
            raise ValueError(init_except_message)
        if not 1 <= rule <= 256:
            raise ValueError(init_except_message)
        
        pattern = {}
        flat_pattern = []
        output_pattern = [int(x) for x in binary_repr(rule, width=8)]

        for i in range(8):
            input_pattern = tuple([int(x) for x in binary_repr(7-i, 3)])
            pattern[input_pattern] = output_pattern[i]
            flat_pattern.extend(input_pattern)
            flat_pattern.append(output_pattern[i])

        self.rule = rule
        self.pattern = pattern
        self.flat_pattern = array(flat_pattern, uint8)

    def __repr__(self) -> str:
        return f'Automata: Rule {self.rule}'
    
    def get_canvas(self, pattern: Pattern|str = Pattern.STANDARD,
                   columns: int = 100) -> 'Canvas':
        """
        Method to generate the typical pattern, starting with a single point.

        `columns` is an `int` of the width that the canvas will be generated to
        """
        return Canvas(self, pattern, columns)
    
    def get_random_canvas(self, columns: int = 100) -> 'Canvas':
        """
        Wrapper method for pre-defined random canvas arguments
        """
        return self.get_canvas(Pattern.RANDOM, columns)