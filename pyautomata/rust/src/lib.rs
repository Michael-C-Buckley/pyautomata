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

fn generate_row(rules_map: &HashMap<(u8 , u8, u8), u8>, input_row: &[u8], output_row: &mut [u8],
    start: usize, stop: usize) -> u32 {
    // Function to generate a single row given proper inputs
    let mut row_sum: u32 = 0;

    for i in start..stop {
        let left = if i == 0 { 0 } else { input_row[i - 1] };
        let center = input_row[i];
        let right = if i == input_row.len() - 1 { 0 } else { input_row[i + 1] };

        if let Some(&new_value) = rules_map.get(&(left as u8, center as u8, right as u8)) {
            output_row[i] = new_value as u8;
            row_sum += new_value as u32;
        }
    }
    row_sum
}

#[no_mangle]
pub extern "C" fn generate_canvas(
    initial_row: *const u8, 
    rows: usize, 
    columns: usize, 
    rules: *const u8,
    rules_length: usize,
    boost: bool,
    central_line: usize,
    whole: bool
) -> CanvasPointers {
    // Determines whether the functions should be broken up
    if whole {
        generate_canvas_whole(initial_row, rows, columns, rules, rules_length, boost, central_line)
    }
    else {
        generate_canvas_by_row(initial_row, rows, columns, rules, rules_length, boost, central_line)
    }
}

fn generate_canvas_by_row(
    initial_row: *const u8, 
    rows: usize, 
    columns: usize, 
    rules: *const u8,
    rules_length: usize,
    boost: bool,
    central_line: usize
) -> CanvasPointers {

    let mut working_canvas = Vec::with_capacity(rows);
    let mut sums = vec![0; rows];

    let (initial_row_slice, rules_slice) = unsafe {
        (
            slice::from_raw_parts(initial_row, columns),
            slice::from_raw_parts(rules, rules_length),
        )
    };

    let rules_map = process_rules(rules_slice);

    let mut first_row_sum: u32 = 0;
    for &value in initial_row_slice.iter() {
        assert!(value == 0 || value == 1, "Initial row must contain only 0s and 1s");
        first_row_sum = first_row_sum + value as u32;
    }
    working_canvas.push(initial_row_slice.to_vec());
    sums[0] = first_row_sum;

    for row in 0..rows-1 {
        let mut output_row = vec![0u8; columns];

        let mut start: usize = 0;
        let mut stop: usize = columns;

        // Boosting masks untouched whitespace when appropriate
        if boost {
            start = central_line.saturating_sub(row + 2);
            stop = std::cmp::min(central_line + row + 2, columns);
        }

        let input_row = &working_canvas[row];

        let row_sum = generate_row(&rules_map, &input_row, &mut output_row, start, stop);

        working_canvas.push(output_row.to_vec());
        sums[row] = row_sum;
    }

    let mut canvas: Vec<u8> = working_canvas.into_iter().flat_map(|row| row.into_iter()).collect();

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

fn generate_canvas_whole(
    initial_row: *const u8, 
    rows: usize, 
    columns: usize, 
    rules: *const u8,
    rules_length: usize,
    boost: bool,
    central_line: usize
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

        let mut start: usize = 0;
        let mut stop: usize = columns;

        // Boosting masks untouched whitespace when appropriate
        if boost {
            start = central_line.saturating_sub(row + 2);
            stop = std::cmp::min(central_line + row + 2, columns);
        }

        for col in start..stop {
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

#[repr(C)]
pub struct StatsStruct {
    standard_deviation: f32,
    mean_increase: f32,
    marginal_sum_increase_ptr: *mut f32,
    sum_rate_length: usize,
}

#[no_mangle]
pub extern "C" fn calculate_stats(canvas_sums: *const u32, sums_length: usize) -> StatsStruct {
    // Stat calculation

    let sums_slice = unsafe {
        slice::from_raw_parts(canvas_sums, sums_length)
    };

    let mut marginal_sum_increase = Vec::new();
    let mut total_sum_increase = 0.0;
    for (i, &sum) in sums_slice.iter().enumerate() {
        if sum != 0 {
            let increase = i as f32 / sum as f32;
            marginal_sum_increase.push(increase);
            total_sum_increase += increase;
        }
    }

    let mean_increase = total_sum_increase / marginal_sum_increase.len() as f32;

    let variance_sum: f32 = marginal_sum_increase.iter().map(|&x| (x - mean_increase).powf(2.0)).sum();
    let standard_deviation = f32::sqrt(variance_sum / marginal_sum_increase.len() as f32);
    
    let sum_rate_length: usize = marginal_sum_increase.len();

    let marginal_sum_increase_ptr = marginal_sum_increase.as_mut_ptr();
    std::mem::forget(marginal_sum_increase);

    StatsStruct {
        standard_deviation: standard_deviation,
        mean_increase: mean_increase,
        marginal_sum_increase_ptr: marginal_sum_increase_ptr,
        sum_rate_length: sum_rate_length,
    }
}

#[no_mangle]
pub extern "C" fn free_memory(ptr: *mut u8, size_in_bytes: usize) {
    // Function to release the memory after it has been transferred into Python-owned memory
    if !ptr.is_null() {
        let _ = unsafe { Vec::from_raw_parts(ptr, size_in_bytes, size_in_bytes) };
    }
}