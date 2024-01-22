# PyAutomata Recognizer Library

# Third-Party Modules
from numpy import ndarray

# Local Modules
from pyautomata.handlers.rust import RUST_AVAILABLE, recognize_canvas

class Recognizer:
    """
    Recognizer is the term to given to the pattern analyzer.  It iterates a canvas
    and returns the number of times repeating segments come up.  It also creates
    a new `rule set` for the new larger pattern size.
    """
    def __init__(self, rule: int, canvas_array: ndarray, pattern_length: int = 5,
                 force_python: bool = False) -> None:

        init_except_message = 'Rule must be an integer between 1 and 256'
        if type(rule) != int:
            raise ValueError(init_except_message)
        if not 1 <= rule <= 256:
            raise ValueError(init_except_message)

        self.rule = rule
        self.canvas_array = canvas_array
        self.input_rows = len(canvas_array)
        self.pattern_length = pattern_length

        self.recognize_canvas(canvas_array, pattern_length, force_python)

    def recognize_canvas(self, canvas_array: ndarray, pattern_length: int = 5,
                         force_python: bool = False):
        """"""

        if RUST_AVAILABLE and not force_python:
            rules_dict, segment_dict, segments = recognize_canvas(canvas_array, len(canvas_array), len(canvas_array[0]), pattern_length)
            self.pattern_rules = rules_dict
            self.pattern_segments = segment_dict
            self.segment_count = segments
        else:
            self.python_recognize_canvas(canvas_array, pattern_length)

    def python_recognize_canvas(self, canvas_array: ndarray, pattern_length: int = 5):
        """
        'Recognition' is a function that searches and return longer pattern sets
        """
        self.pattern_segments: dict[tuple[int], int] = {}
        self.pattern_rules: dict[tuple[int], tuple[int]] = {}
        self.segment_count = 0
        for i in range(1, len(canvas_array)):
            row = canvas_array[i]
            for j in range(1, len(row)):
                if j + pattern_length > len(row):
                    continue
                segment = tuple(row[j:j+pattern_length])

                self.segment_count += 1

                if segment in self.pattern_segments:
                    self.pattern_segments[segment] += 1
                else:
                    parent_pattern = tuple(canvas_array[i-1][j-1:j+len(segment)+1])
                    if len(parent_pattern) != pattern_length + 2:
                        continue
                    self.pattern_segments[segment] = 1
                    self.pattern_rules[parent_pattern] = segment
