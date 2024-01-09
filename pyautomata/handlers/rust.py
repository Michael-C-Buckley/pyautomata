# Project PyAutomata Python-Rust Integration Module

# Python Modules
from ctypes import POINTER, c_size_t, c_uint8, CDLL

# Third-Party Modules
from numpy import ctypeslib, ndarray, copyto, zeros, uint8
from icecream import ic

lib = CDLL('pyautomata/rust/target/release/libpyautomata_rust.so')

lib.generate_canvas.argtypes = [
    POINTER(c_uint8),  # initial_row
    c_size_t,          # rows
    c_size_t,          # columns
    POINTER(c_uint8),  # rules
    c_size_t           # rules_length
]

lib.generate_canvas.restype = POINTER(c_uint8)

lib.free_canvas.argtypes = [
    POINTER(c_uint8),  # pointer
    c_size_t           # size
]

def generate_canvas(initial_row: ndarray, rows: int, columns: int, rules: dict[tuple[int], int]):
    """
    Python API for Rust FFI to generate the canvas
    """
    # Create pointers
    initial_row_pointer = initial_row.ctypes.data_as(POINTER(c_uint8))
    rules_pointer = rules.ctypes.data_as(POINTER(c_uint8))

    # Perform the calculations in Rust and get the pointer to the results
    canvas_pointer = lib.generate_canvas(initial_row_pointer, rows, columns, rules_pointer, len(rules))
    canvas_result = ctypeslib.as_array(canvas_pointer, shape=(rows, columns))
    
    # Move the data into Python-owned memory
    canvas = zeros((rows, columns), dtype=uint8)
    copyto(canvas, canvas_result)

    # Free the memory allocated in Rust after translation
    lib.free_canvas(canvas_pointer, rows * columns)

    return canvas

