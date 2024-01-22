# Project PyAutomata Recognizer Tests

# Python Modules
from unittest import TestCase, main
from copy import deepcopy

# Third-Party Modules

# Local Modules
from pyautomata import Recognizer
from tests.test_common import RULE_30_STANDARD

EXPECTED_PATTERNS = {
    (0, 0, 0, 0, 0, 1, 0): (0, 0, 0, 1, 1),
    (0, 0, 0, 0, 1, 0, 0): (0, 0, 1, 1, 1),
    (0, 0, 0, 1, 0, 0, 0): (0, 1, 1, 1, 0),
    (0, 0, 1, 0, 0, 0, 0): (1, 1, 1, 0, 0),
    (0, 0, 0, 0, 1, 1, 1): (0, 0, 1, 1, 0),
    (0, 0, 0, 1, 1, 1, 0): (0, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0): (1, 1, 0, 0, 1),
    (0, 1, 1, 1, 0, 0, 0): (1, 0, 0, 1, 0),
    (0, 0, 0, 1, 1, 0, 0): (0, 1, 1, 0, 1),
    (0, 0, 1, 1, 0, 0, 1): (1, 1, 0, 1, 1),
    (0, 1, 1, 0, 0, 1, 0): (1, 0, 1, 1, 1),
    (1, 1, 0, 0, 1, 0, 0): (0, 1, 1, 1, 1),
    (0, 0, 1, 1, 0, 1, 1): (1, 1, 0, 0, 1),
    (0, 1, 1, 0, 1, 1, 1): (1, 0, 0, 1, 0),
    (1, 1, 0, 1, 1, 1, 1): (0, 0, 1, 0, 0),
    (1, 0, 1, 1, 1, 1, 0): (0, 1, 0, 0, 0), 
}

class RecognizerTestCase(TestCase):
    def test_recognizer_validation(self):
        for bad_case in [500, 'abc']:
            with self.assertRaises(ValueError):
                Recognizer(bad_case, None)

    def recognition_results(self, force_python: bool):
        """
        Support function to de-duplicate code in Python and Rust tests
        """
        recognizer = Recognizer(30, RULE_30_STANDARD, force_python=force_python)
        self.assertEqual(recognizer.pattern_rules, EXPECTED_PATTERNS)

    def test_python_recognition(self):
        self.recognition_results(True)

    def test_rust_recognition(self):
        self.recognition_results(False)


if __name__ == '__main__':
    main()