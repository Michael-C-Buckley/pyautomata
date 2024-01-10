// PyAutomata Rust Support Library

use std::collections::HashMap;
use std::slice;

#[repr(C)]
pub struct CanvasPointers {
    canvas_pointer: *mut u8,
    sums_pointer: *mut u32,
}

fn process_rules(rules: &[u8]) -> HashMap<(u8 , u8, u8), u8> {
    // Convert and create a hash map from the rules
    let mut rules_map = HashMap::new();

    // Rules are 4 members, 3 inputs and 1 output
    for chunk in rules.chunks_exact(4) {
        for &value in chunk {
            assert!(value == 0 || value == 1, "Pattern rules must be either 0 or 1");
        }
        let key = (chunk[0], chunk[1], chunk[2]);
        let value = chunk[3];
        rules_map.insert(key, value);
    }
    
    rules_map
}

#[no_mangle]
pub extern "C" fn generate_canvas(
    initial_row: *const u8, 
    rows: usize, 
    columns: usize, 
    rules: *const u8,
    rules_length: usize
) -> CanvasPointers {

    let mut canvas = vec![0; rows * columns];
    let mut sums = vec![0; rows];

    let (initial_row_slice, rules_slice) = unsafe {
        (
            slice::from_raw_parts(initial_row, columns),
            slice::from_raw_parts(rules, rules_length),
        )
    };

    let rules_map = process_rules(rules_slice);

    let mut first_row_sum: u32 = 0;
    for (i, &value) in initial_row_slice.iter().enumerate() {
        assert!(value == 0 || value == 1, "Initial row must contain only 0s and 1s");
        canvas[i] = value as u8;
        first_row_sum = first_row_sum + value as u32;
    }
    sums[0] = first_row_sum;

    for row in 0..rows-1 {
        let mut row_sum: u32 = 0;
        for col in 0..columns {
            let left = if col == 0 { 0 } else { canvas[row * columns + col - 1] };
            let center = canvas[row * columns + col];
            let right = if col == columns - 1 { 0 } else { canvas[row * columns + col + 1] };
    
            if let Some(&new_value) = rules_map.get(&(left as u8, center as u8, right as u8)) {
                canvas[(row + 1) * columns + col] = new_value as u8;
                row_sum = row_sum + new_value as u32;
            }
        sums[row] = row_sum;
        }
    }
    // Capture the pointers and forget them to prevent automatic memory management
    let canvas_ptr = canvas.as_mut_ptr();
    let sums_ptr = sums.as_mut_ptr();
    std::mem::forget(canvas);
    std::mem::forget(sums);

    CanvasPointers {
        canvas_pointer: canvas_ptr,
        sums_pointer: sums_ptr
    }
}

#[no_mangle]
pub extern "C" fn free_memory(ptr: *mut u8, size_in_bytes: usize) {
    // Function to release the memory after it has been transferred into Python-owned memory
    if !ptr.is_null() {
        let _ = unsafe { Vec::from_raw_parts(ptr, size_in_bytes, size_in_bytes) };
    }
}