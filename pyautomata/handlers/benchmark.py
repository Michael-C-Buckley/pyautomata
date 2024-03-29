# Project PyAutomata Benchmarking Module

# Python Modules
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from time import perf_counter, sleep

# Local Modules
from pyautomata.classes.canvas import Canvas
from pyautomata.handlers.rust import RUST_AVAILABLE

class Engine(Enum):
    PYTHON = 'Python'
    RUST = 'Rust'

@dataclass
class CalculationData:
    engine: Engine
    rule: int
    data: dict[int, float]
    created: datetime

def benchmark_calculation(engine: Engine, start: int = 100, stop: int = 1000,
                          step: int = 100, rule: int = 30) -> CalculationData:
    """
    Generate data on the time it takes to generate canvases
    """
    engine_map = {
        Engine.RUST: False,
        Engine.PYTHON: True,
    }

    if engine is Engine.RUST and not RUST_AVAILABLE:
        raise RuntimeError('Rust cannot be calculated if the libraries did not load correctly')

    calculation_dict: dict[int, float] = {}

    for i in range(start, stop+step, step):
        print(f'Working on: {i} in {engine.value} --------', end='\r')
        start_time = perf_counter()
        Canvas(rule, i, force_python=engine_map.get(engine))
        calculation_dict[i] = perf_counter() - start_time

    print(f'Completed {engine.value} generation -------------', end='\r')

    return CalculationData(engine, rule, calculation_dict, datetime.now())
        
def get_comparison_benchmarks(start: int = 100, stop: int = 1000,
                          step: int = 100, rule: int = 30) -> tuple[CalculationData, CalculationData]:
    """
    Simple function to get results for both Rust and Python
    """
    generate = lambda local_engine: benchmark_calculation(local_engine, start, stop, step, rule)
    result = (generate(Engine.RUST), generate(Engine.PYTHON))
    print('Completed generation benchmarks for both Rust and Python.')
    return result