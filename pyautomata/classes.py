# Cellular Automata

from numpy import arange, binary_repr, zeros

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
        return Canvas(self, description, columns)

class Canvas:
    def __init__(self, automata: Automata, description: str = '', columns: int = 100) -> None:
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