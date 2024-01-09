// PyAutomata Rust Support Library

use std::collections::HashMap;
use std::slice;

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
) -> *mut u8 {

    let mut canvas = vec![0; rows * columns];

    unsafe {
        let initial_row_slice = slice::from_raw_parts(initial_row, columns);
        let rules_slice = slice::from_raw_parts(rules, rules_length);

        let rules_map = process_rules(rules_slice);

        for (i, &value) in initial_row_slice.iter().enumerate() {
            assert!(value == 0 || value == 1, "Initial row must contain only 0s and 1s");
            canvas[i] = value as u8;
        }

        for row in 0..rows-1 {
            for col in 0..columns {
                let left = if col == 0 { 0 } else { canvas[row * columns + col - 1] };
                let center = canvas[row * columns + col];
                let right = if col == columns - 1 { 0 } else { canvas[row * columns + col + 1] };
        
                if let Some(&new_value) = rules_map.get(&(left as u8, center as u8, right as u8)) {
                    canvas[(row + 1) * columns + col] = new_value as u8;
                }
            }
        }
    }
    
    // Prevent Rust from freeing the memory when `canvas` goes out of scope
    let ptr = canvas.as_mut_ptr();
    std::mem::forget(canvas);

    ptr
}

#[no_mangle]
pub extern "C" fn free_canvas(ptr: *mut u8, size: usize) {
    unsafe {
        let _ = Vec::from_raw_parts(ptr, size, size);
    }
}