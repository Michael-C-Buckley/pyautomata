# Project PyAutomata Python-Rust Integration Module

# Python Modules
from ctypes import (
    POINTER, sizeof, cast, CDLL, Structure,
    c_bool, c_size_t, c_uint8, c_uint32, c_float
)

# Third-Party Modules
from numpy import ctypeslib, ndarray, copyto, zeros, uint8, uint32, float32

lib = CDLL('pyautomata/rust/target/release/libpyautomata_rust.so')


class CanvasPointers(Structure):
    _fields_ = [
        ("canvas_pointer", POINTER(c_uint8)),
        ("sums_pointer", POINTER(c_uint32))
    ]

class StatsStructure(Structure):
    _fields_ = [
        ("standard_deviation", c_float),
        ("standard_deviation_sum", c_float),
        ("sums_mean", c_float),
        ("sum_rate_average_ptr", POINTER(c_float)),
        ("sum_rate_length", c_size_t)
    ]

# Generate Canvas
lib.generate_canvas.argtypes = [
    POINTER(c_uint8),  # initial_row
    c_size_t,          # rows
    c_size_t,          # columns
    POINTER(c_uint8),  # rules
    c_size_t,          # rules_length
    c_bool,            # boost
    c_size_t           # central line
]

lib.generate_canvas.restype = CanvasPointers

# Calculate Stats
lib.calculate_stats.argtypes = [
    POINTER(c_uint32), # canvas_sums
    c_size_t           # sums_length 
]

lib.calculate_stats.restype = StatsStructure

# Free Memory
lib.free_memory.argtypes = [
    POINTER(c_uint8),  # pointer
    c_size_t           # size
]

def compute_stats(canvas_sums: ndarray):
    """
    Python API for Rust FFI to calculate stats
    """
    # Create outbound pointer
    canvas_sums_pointer = canvas_sums.ctypes.data_as(POINTER(c_uint32))
    
    # Perform the calculations
    stats_results: StatsStructure = lib.calculate_stats(canvas_sums_pointer, len(canvas_sums))
    
    # Move data into Python-owned memory space
    sum_shape = (stats_results.sum_rate_length,)
    sum_rate_average = zeros(sum_shape, dtype=float32)
    sum_rate_result = ctypeslib.as_array(stats_results.sum_rate_average_ptr, shape=sum_shape)
    copyto(sum_rate_average, sum_rate_result)

    # Free the memory allocated in Rust after translation
    free_memory(stats_results.sum_rate_average_ptr, c_uint32, stats_results.sum_rate_length)
    
    standard_deviation = stats_results.standard_deviation
    standard_deviation_sum = stats_results.standard_deviation_sum
    sums_mean = stats_results.sums_mean

    return sum_rate_average, standard_deviation_sum, sums_mean, standard_deviation

def free_memory(pointer, dtype, num_elements):
    """
    Free memory allocated in Rust for arrays of different types.
    """
    size_in_bytes = sizeof(dtype) * num_elements
    pointer_as_u8 = cast(pointer, POINTER(c_uint8))
    lib.free_memory(pointer_as_u8, size_in_bytes)

def generate_canvas(initial_row: ndarray, rows: int, columns: int,
                    rules: dict[tuple[int], int,],
                    boost: bool = False, central_line: int = 0):
    """
    Python API for Rust FFI to generate the canvas
    """
    # Create outbound pointers
    initial_row_pointer = initial_row.ctypes.data_as(POINTER(c_uint8))
    rules_pointer = rules.ctypes.data_as(POINTER(c_uint8))

    # Perform the calculations in Rust and get the pointer to the results
    pointers: CanvasPointers = lib.generate_canvas(initial_row_pointer, rows, columns, rules_pointer, len(rules), boost, central_line)
    canvas_result = ctypeslib.as_array(pointers.canvas_pointer, shape=(rows, columns))
    sums_result = ctypeslib.as_array(pointers.sums_pointer, shape = (rows,))
    
    # Move the data into Python-owned memory
    canvas = zeros((rows, columns), dtype=uint8)
    copyto(canvas, canvas_result)
    sums_array = zeros((rows,), dtype=uint32)
    copyto(sums_array, sums_result)

    # Free the memory allocated in Rust after translation
    free_memory(pointers.canvas_pointer, c_uint8, rows * columns)
    free_memory(pointers.sums_pointer, c_uint32, rows)

    return canvas, sums_array

