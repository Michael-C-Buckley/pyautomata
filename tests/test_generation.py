# PyAutomata Classes Tests

# Python Modules
from unittest import TestCase, main

# Third-Party Modules
from numpy import array_equal

# Local Modules
from tests.common import PATTERN_TEST_MAP
from pyautomata.classes import Canvas, Pattern

class GenerationTestCase(TestCase):
    """
    Tests related to canvas generation
    """
    def check_canvas_array(self, input_pattern: str|Pattern,
                           matching_pattern: str|Pattern = None,
                           force_python: bool = False) -> bool:
        """
        Method to generate and return test canvases for evaluation
        """
        if matching_pattern is None:
            matching_pattern = PATTERN_TEST_MAP.get(input_pattern)
            
        result = Canvas(30, 5, input_pattern, force_python).result

        if not array_equal(result, matching_pattern):
            if result.shape != matching_pattern.shape:
                return False
            for a, b in zip(result.flatten(), matching_pattern.flatten()):
                if a != b:
                    return False
                
        return True

    def test_invalid_canvas(self):
        for bad_case in [1000, 'ABC']:
            with self.assertRaises(ValueError):
                Canvas(bad_case)

    def test_invalid_pattern(self):
        with self.assertRaises(ValueError):
            Pattern.from_string('asdf')

    # GENERATION TESTS

    def test_rust_generation_standard(self):
        test_result = self.check_canvas_array(Pattern.STANDARD)
        self.assertEqual(test_result, True)

    def test_rust_generation_right(self):
        for test_case in [Pattern.RIGHT, 'right']:
            test_result = self.check_canvas_array(test_case)
            self.assertEqual(test_result, True)

    def test_rust_generation_alternating(self):
        test_result = self.check_canvas_array(Pattern.ALTERNATING)
        self.assertEqual(test_result, True)

    def test_python_generation_standard(self):
        test_result = self.check_canvas_array(Pattern.STANDARD, force_python=True)
        self.assertEqual(test_result, True)

    def test_python_generation_right(self):
        for test_case in [Pattern.RIGHT, 'right']:
            test_result = self.check_canvas_array(test_case, force_python=True)
            self.assertEqual(test_result, True)

    def test_python_generation_alternating(self):
        test_result = self.check_canvas_array(Pattern.ALTERNATING, force_python=True)
        self.assertEqual(test_result, True)


if __name__ == '__main__':
    main()