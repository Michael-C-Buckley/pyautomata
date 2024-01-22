# PyAutomata Common Test Module

# Python Modules

# Third-Party Modules
from numpy import array, uint8

# Local Modules
from pyautomata import Pattern

# Rule 30, 5 Rows for calculation
RULE_30_STANDARD = array([
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0, 0, 1, 0, 0,
    0, 0, 1, 1, 0, 1, 1, 1, 1, 0,
    0, 1, 1, 0, 0, 1, 0, 0, 0, 1,
], uint8).reshape(5, 10)

RULE_30_RIGHT = array([
    0, 0, 0, 0, 1,
    0, 0, 0, 1, 1,
    0, 0, 1, 1, 0,
    0, 1, 1, 0, 1,
    1, 1, 0, 0, 1,
], uint8).reshape(5, 5)

RULE_30_ALTERNATING = array([
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
    1, 1, 0, 1, 0, 1, 0, 1, 0, 1,
    1, 0, 0, 1, 0, 1, 0, 1, 0, 1,
    1, 1, 1, 1, 0, 1, 0, 1, 0, 1,
    1, 0, 0, 0, 0, 1, 0, 1, 0, 1,
], uint8).reshape(5, 10)

PATTERN_TEST_MAP = {
    Pattern.STANDARD: RULE_30_STANDARD,
    'right': RULE_30_RIGHT,
    Pattern.RIGHT: RULE_30_RIGHT,
    Pattern.ALTERNATING: RULE_30_ALTERNATING,
}