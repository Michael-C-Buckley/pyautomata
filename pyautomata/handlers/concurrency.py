# Project PyAutomata Concurrency Handler

# Python Modules
from functools import lru_cache
from multiprocessing import Pool, Queue
from typing import Any, Callable


def worker(queue: Queue):
    """
    Loopable function for the calculation workers
    """
    while True:
        task = queue.get()
        if task is None:
            break

        func, param = task
        func(param)

class CalculationPool:
    def __init__(self, workers_num: int = 4) -> None:
        self.pool = Pool(workers_num)
        self.queue = Queue()
        self.workers = [self.pool.apply_async(worker, (self.queue,)) for i in range(workers_num)]


@lru_cache
def get_calculation_pool(workers_num: int = 4) -> CalculationPool:
    """
    Function that starts and caches pools to de-duplicate start-up overhead costs
    """
    return CalculationPool(workers_num)

def execute(task_list: list[Any], func: Callable, workers_num: int = 8):
    """
    Execute tasks in a process pool
    """
    pool = get_calculation_pool(workers_num)

