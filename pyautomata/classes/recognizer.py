# PyAutomata Recognizer Library

# Third-Party Modules
from numpy import ndarray

class Recognizer:
    """
    Recognizer is the term to given to the pattern analyzer.  It iterates a canvas
    and returns the number of times repeating segments come up.  It also creates
    a new `rule set` for the new larger pattern size.
    """
    def __init__(self, rule: int, canvas_array: ndarray, pattern_length: int = 5) -> None:

        init_except_message = 'Rule must be an integer between 1 and 256'
        if type(rule) != int:
            raise ValueError(init_except_message)
        if not 1 <= rule <= 256:
            raise ValueError(init_except_message)

        self.rule = rule
        self.canvas_array = canvas_array
        self.input_rows = len(canvas_array)
        self.pattern_length = pattern_length

        pattern_rules, pattern_segments, segment_count = self.python_recognize_canvas(canvas_array, pattern_length)

        self.pattern_segments = pattern_segments
        self.pattern_rules = pattern_rules
        self.segment_count = segment_count

    @staticmethod
    def python_recognize_canvas(canvas_array: ndarray, pattern_length: int = 5):
        """
        'Recognition' is a function that searches and return longer pattern sets
        """
        pattern_segments: dict[tuple[int], int] = {}
        pattern_rules: dict[tuple[int], tuple[int]] = {}
        segment_count = 0
        for i in range(1, len(canvas_array)):
            row = canvas_array[i]
            for j in range(1, len(row)):
                if j + pattern_length > len(row):
                    continue
                segment = tuple(row[j:j+pattern_length+1])

                segment_count += 1

                if segment in pattern_segments:
                    pattern_segments[segment] += 1
                else:
                    parent_pattern = tuple(canvas_array[i-1][j-1:j+len(segment)+1])
                    pattern_segments[segment] = 1
                    pattern_rules[parent_pattern] = segment

        return pattern_rules, pattern_segments, segment_count
