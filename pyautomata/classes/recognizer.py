# PyAutomata Recognizer Library

# Third-Party Modules
from numpy import ndarray

# Local Modules
from pyautomata.handlers.rust import RUST_AVAILABLE, recognize_canvas
from pyautomata.classes.general import Pattern, CENTRAL_LINE_MAP

class Recognizer:
    """
    Recognizer is the term to given to the pattern analyzer.  It iterates a canvas
    and returns the number of times repeating segments come up.  It also creates
    a new `rule set` for the new larger pattern size.
    """
    def __init__(self, rule: int, canvas_array: ndarray, canvas_pattern: Pattern = None,
                 pattern_length: int = 5, force_python: bool = False) -> None:

        init_except_message = 'Rule must be an integer between 1 and 256'
        if type(rule) != int:
            raise ValueError(init_except_message)
        if not 1 <= rule <= 256:
            raise ValueError(init_except_message)

        self.rule = rule
        self.canvas_array = canvas_array
        self.input_rows = len(canvas_array)
        self.pattern_length = pattern_length
        self.canvas_pattern = canvas_pattern

        boost = True if canvas_pattern in CENTRAL_LINE_MAP else False
        central_line = 0 if not boost else CENTRAL_LINE_MAP[canvas_pattern](len(canvas_array[0]))

        self.recognize_canvas(canvas_array, pattern_length, force_python, boost, central_line)

    def recognize_canvas(self, canvas_array: ndarray, pattern_length: int = 5,
                         force_python: bool = False, boost: bool = False,
                         central_line: int = 0) -> None:
        """
        Wrapper for generating the analysis either with Rust or Python
        """
        # Collect kwargs from the signature
        kwargs = {k:v for k,v in locals().items() if k not in ['self', 'force_python']}

        if RUST_AVAILABLE and not force_python:
            rules_dict, segment_dict, segments = recognize_canvas(canvas_array.shape, **kwargs)
            self.pattern_rules = rules_dict
            self.pattern_segments = segment_dict
            self.segment_count = segments
        else:
            self.python_recognize_canvas(**kwargs)

    def python_recognize_canvas(self, canvas_array: ndarray, pattern_length: int = 5,
                                boost: bool = False, central_line: int = 0) -> None:
        """
        'Recognition' is a function that searches and return longer pattern sets
        """
        self.pattern_segments: dict[tuple[int], int] = {}
        self.pattern_rules: dict[tuple[int], tuple[int]] = {}
        self.segment_count = 0

        for i in range(1, len(canvas_array)):

            stop_default = len(canvas_array[i])-pattern_length
            start = (central_line - i - 2) if boost else 1
            stop = min(central_line + i + 2, stop_default) if boost else stop_default
            
            # for j in range(1, len(canvas_array[i])-pattern_length):
            for j in range(start, stop):

                segment = tuple(canvas_array[i][j:j+pattern_length])
                parent_pattern = tuple(canvas_array[i-1][j-1:j+len(segment)+1])
                self.segment_count += 1
                self.pattern_rules[parent_pattern] = segment

                if segment in self.pattern_segments:
                    self.pattern_segments[segment] += 1
                else:
                    self.pattern_segments[segment] = 1