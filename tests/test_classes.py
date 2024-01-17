# PyAutomata Classes Tests

# Python Modules
from unittest import TestCase, main

# Third-Party Modules
from numpy import array_equal

# Local Modules
from tests.test_common import (
    PATTERN_TEST_MAP
)
from pyautomata.classes import Canvas, Pattern

class ClassesTestCase(TestCase):
    """"""
    def check_canvas_array(self, matching_pattern, input_pattern: str|Pattern = Pattern.STANDARD,
                         force_python: bool = False):
        """
        Method to generate and return test canvases for evaulation
        """
        result = Canvas(30, 5, input_pattern, force_python).result
        return array_equal(result, matching_pattern)

    def test_invalid_cases(self):
        """
        Simple test for invalid cases on `Canvas` and `Pattern`
        """
        for bad_case in [1000, 'ABC']:
            with self.assertRaises(ValueError):
                Canvas(bad_case)

        with self.assertRaises(ValueError):
            Pattern.from_string('asdf')

    def test_canvas_rust_generate(self):
        """
        Rust generation logic test
        """
        for pattern, matching_pattern in PATTERN_TEST_MAP.items():
            test_result = self.check_canvas_array(matching_pattern, pattern)
            self.assertEqual(test_result, True)


    def test_canvas_python_generate(self):
        """
        Python generation logic tests
        """
        for pattern, matching_pattern in PATTERN_TEST_MAP.items():
            test_result = self.check_canvas_array(matching_pattern, pattern, True)
            self.assertEqual(test_result, True)

    def test_canvas_render(self):
        """"""

    def test_canvas_draw_sums_deviations(self):
        """"""

if __name__ == '__main__':
    main()