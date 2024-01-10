# Project PyAutomata Stats Module

# Python Modules
from dataclasses import dataclass
from functools import cached_property
from math import sqrt
from typing import TYPE_CHECKING

# Third-Party Modules
from numpy import linspace, isnan
from icecream import ic

# Local Modules
if TYPE_CHECKING:
    from pyautomata.classes.canvas import Canvas

# Stats for Sums

@dataclass
class StatsContainer:
    sum_rate_average: list[float]
    standard_deviation_sum: float
    mean: float
    standard_deviation: float

    def offset_standard_deviation(self, factor: int):
        return self.standard_deviation * factor
    
    @cached_property
    def standard_deviations_map(self) -> dict[int, float]:
        standard_deviations = {}
        for i in range(-3, 4):
            if i == 0:
                continue
            standard_deviations[i] = self.mean + self.offset_standard_deviation(i)
        return standard_deviations


def calculate_stats(canvas: 'Canvas') -> StatsContainer:
    y = linspace(0, canvas.columns, canvas.columns)

    total_sums = 0
    standard_deviation_sum = 0

    sum_rate_average = []
    for i in range(len(canvas.sums)):
        canvas_value = canvas.sums[i]
        if canvas_value == 0:
            continue
        result = i/canvas.sums[i]
        result = result if not isnan(result) else 0.0
        sum_rate_average.append(result)
        total_sums =+ i

    sums_mean = total_sums/len(canvas.sums)
    distance_from_mean = []

    for i in sum_rate_average:
        var = (i - sums_mean)
        distance_from_mean.append(var)
        var = abs(var) ** 2
        standard_deviation_sum += var

    standard_deviation = sqrt(standard_deviation_sum/len(canvas.sums))

    return StatsContainer(sum_rate_average, standard_deviation_sum,
                          sums_mean, standard_deviation)