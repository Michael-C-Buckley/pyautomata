# Project PyAutomata Stats Module

# Python Modules
from dataclasses import dataclass
from functools import cached_property
from math import sqrt
from typing import TYPE_CHECKING

# Local Modules
if TYPE_CHECKING:
    from pyautomata.classes.canvas import Canvas

# Foreign Function Interfacing and checking
from pyautomata.handlers import compute_stats, RUST_AVAILABLE

# Stats for Sums

@dataclass
class StatsContainer:
    marginal_sum_increase: list[float]
    mean_increase: float
    standard_deviation: float

    def offset_increase_standard_deviation(self, factor: int):
        return self.standard_deviation * factor
    
    @cached_property
    def increase_standard_deviations_map(self) -> dict[int, float]:
        standard_deviations = {}
        for i in range(-3, 4):
            if i == 0:
                continue
            standard_deviations[i] = self.mean_increase + self.offset_increase_standard_deviation(i)
        return standard_deviations

def calculate_stats(canvas: 'Canvas') -> StatsContainer:
    """
    Rust-powered API for calculating stats
    """
    if RUST_AVAILABLE:
        results = compute_stats(canvas.sums)
        return StatsContainer(*results)
    else:
        return python_calculate_stats(canvas)


def python_calculate_stats(canvas: 'Canvas') -> StatsContainer:
    """
    Native Python API for calculating stats if Rust is not available
    """
    marginal_sum_increase = []
    total_sum_increase = 0

    for i, sum_value in enumerate(canvas.sums):
        if sum_value != 0:
            increase = i / sum_value
            marginal_sum_increase.append(increase)
            total_sum_increase += increase

    mean_increase = total_sum_increase / len(marginal_sum_increase)

    variance_sum = sum((x - mean_increase) ** 2 for x in marginal_sum_increase)
    standard_deviation = sqrt(variance_sum / len(marginal_sum_increase))

    return StatsContainer(marginal_sum_increase, mean_increase, standard_deviation)