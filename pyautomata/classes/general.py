from enum import Enum

class Pattern(Enum):
    ALTERNATING = 'Alternating First Row'
    RANDOM = 'Random First Row'
    STANDARD = 'Standard Center Start'
    LEFT = 'Left Start'
    RIGHT = 'Right Start'

    @classmethod
    def from_string(cls, input_string: str):
        """
        Basic conversion method for mapping strings to values
        """
        string_map: dict = {
            'alternating': cls.ALTERNATING,
            'random': cls.RANDOM,
            'left': cls.LEFT,
            'right': cls.RIGHT,
            'standard': cls.STANDARD,
        }

        if (pattern_match := string_map.get(input_string)):
            return pattern_match
        else:
            raise ValueError(f'No Pattern with the value: {input_string}')
