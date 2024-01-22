# Project PyAutomata Python-Rust Integration Module

# Python Modules
from ctypes import (
    POINTER, sizeof, cast, string_at, CDLL, Structure, c_char,
    c_bool, c_size_t, c_uint8, c_uint32, c_float
)
from json import loads
from os import path

# Third-Party Modules
from numpy import ctypeslib, ndarray, copyto, zeros, uint8, uint32, float32


# Path construction

# Docker path
rust_path = '/rust/target/release/libpyautomata_rust.so'
library_path = f'/app/pyautomata{rust_path}'

# Locally install path
if not path.exists(library_path):
    current_path = path.dirname(path.abspath(__file__))
    files_path = path.abspath(path.join(current_path, '..'))
    library_path = f'{files_path}{rust_path}'

try:
    lib = CDLL(library_path)
    RUST_AVAILABLE = True
except (OSError, ImportError) as e:
    """
    Failure to import will create a dummy instance to accept modification and
    not error, however, the global constant will be referenced by anything that
    uses Rust FFI APIs and will default to Python logic if not available
    """
    print(e)
    RUST_AVAILABLE = False
    from unittest.mock import Mock
    from warnings import warn
    warn('PyAutomata: Rust binary not found, falling back on Python logic')
    lib = Mock()


class CanvasPointers(Structure):
    _fields_ = [
        ('canvas_pointer', POINTER(c_uint8)),
        ('sums_pointer', POINTER(c_uint32))
    ]

class StatsStructure(Structure):
    _fields_ = [
        ('standard_deviation', c_float),
        ('mean_increase', c_float),
        ('marginal_sum_increase_ptr', POINTER(c_float)),
        ('sum_rate_length', c_size_t)
    ]

class RecognitionOutput(Structure):
    _fields_ = [
        ('pattern_rules_pointer', POINTER(c_char)),
        ('pattern_segments_pointer', POINTER(c_char)),
        ('segment_count', c_size_t),
        ('pattern_rules_length', c_size_t),
        ('pattern_segments_legnth', c_size_t)
    ]

# Generate Canvas
lib.generate_canvas.argtypes = [
    POINTER(c_uint8),  # initial_row
    c_size_t,          # rows
    c_size_t,          # columns
    POINTER(c_uint8),  # rules
    c_size_t,          # rules_length
    c_bool,            # boost
    c_size_t,          # central_line
    c_bool             # whole
]

lib.generate_canvas.restype = CanvasPointers

# Calculate Stats
lib.calculate_stats.argtypes = [
    POINTER(c_uint32), # canvas_sums
    c_size_t           # sums_length 
]

lib.calculate_stats.restype = StatsStructure

# Recognize Canvas
lib.recognize_canvas.argtypes = [
    POINTER(c_uint8),  # canvas_pointer
    c_size_t,          # rows
    c_size_t,          # columns
    c_size_t,          # pattern_length
]

lib.recognize_canvas.restype = RecognitionOutput

# Free Memory
lib.free_memory.argtypes = [
    POINTER(c_uint8),  # pointer
    c_size_t           # size
]

# Free String
lib.free_string.argtypes = [
    POINTER(c_char)    # pointer
]

def free_memory(pointer, dtype, num_elements):
    """
    Free memory allocated in Rust for arrays of different types.
    """
    size_in_bytes = sizeof(dtype) * num_elements
    pointer_as_u8 = cast(pointer, POINTER(c_uint8))
    lib.free_memory(pointer_as_u8, size_in_bytes)

def free_string(pointer):
    """
    Free memory allocated to Rust/C-strings
    """
    lib.free_string(pointer)


def compute_stats(canvas_sums: ndarray) -> tuple[ndarray[float32], float, float]:
    """
    Python API for Rust FFI to calculate stats
    """
    # Create outbound pointer
    canvas_sums_pointer = canvas_sums.ctypes.data_as(POINTER(c_uint32))
    
    # Perform the calculations
    stats_results: StatsStructure = lib.calculate_stats(canvas_sums_pointer, len(canvas_sums))
    
    # Move data into Python-owned memory space
    sum_shape = (stats_results.sum_rate_length,)
    marginal_sum_increase = zeros(sum_shape, dtype=float32)
    sum_rate_result = ctypeslib.as_array(stats_results.marginal_sum_increase_ptr, shape=sum_shape)
    copyto(marginal_sum_increase, sum_rate_result)

    # Free the memory allocated in Rust after translation
    free_memory(stats_results.marginal_sum_increase_ptr, c_uint32, stats_results.sum_rate_length)
    
    standard_deviation = stats_results.standard_deviation
    mean_increase = stats_results.mean_increase

    return marginal_sum_increase, mean_increase, standard_deviation

def generate_canvas(initial_row: ndarray, rows: int, columns: int,
                    rules: dict[tuple[int], int,], boost: bool = False,
                    central_line: int = 0, whole: bool = True):
    """
    Python API for Rust FFI to generate the canvas
    """
    # Create outbound pointers
    initial_row_pointer = initial_row.ctypes.data_as(POINTER(c_uint8))
    rules_pointer = rules.ctypes.data_as(POINTER(c_uint8))

    # Perform the calculations in Rust and get the pointer to the results
    pointers: CanvasPointers = lib.generate_canvas(initial_row_pointer, rows, columns, rules_pointer, len(rules), boost, central_line, whole)
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

def recognize_canvas(canvas_array: ndarray, rows: int, columns: int, pattern_length: int):
    """
    Python API for Rust FFI for running recognition
    """
    # Prepare outbound information
    canvas_pointer = canvas_array.ctypes.data_as(POINTER(c_uint8))

    # Execute
    results: RecognitionOutput = lib.recognize_canvas(canvas_pointer, rows, columns, pattern_length)
    rules_json = loads(string_at(results.pattern_rules_pointer).decode('utf-8'))
    segments_json = loads(string_at(results.pattern_segments_pointer).decode('utf-8'))

    # Convert to Python Dictionaries
    rules_dict = {}
    segments_dict = {}

    for k, v in rules_json.items():
        new_key = tuple(loads(k))
        new_value = tuple(loads(v))
        rules_dict[new_key] = new_value

    for k, v in segments_json.items():
        new_key = tuple(loads(k))
        segments_dict[new_key] = v

    # Free memory
    free_string(results.pattern_rules_pointer)
    free_string(results.pattern_segments_pointer)

    return rules_dict, segments_dict, results.segment_count
