# Rust Forecast

A Rust-based forecasting library with Python bindings using PyO3 and Maturin.

## Overview

This crate provides a simple forecasting prediction function implemented in Rust with Python bindings. The current implementation is a mock that returns the input values multiplied by 1.0 (i.e., returns the same values).

## Features

- Pure Rust implementation for high performance
- Python bindings via PyO3
- Type-safe prediction interface
- Comprehensive unit tests

## Building and Testing

### Prerequisites

- Rust (1.56 or later)
- Python (3.7 or later)
- Maturin (for building Python wheels)

### Building the Rust Library

```bash
# Build the Rust library
cargo build

# Build in release mode for better performance
cargo build --release
```

### Running Rust Tests

```bash
# Run all unit tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Run a specific test
cargo test test_predict_valid_input
```

### Building Python Bindings

Install maturin if you don't have it:

```bash
pip install maturin
```

#### Development Mode

For local development and testing:

```bash
# Install the package in development mode
maturin develop

# Or with release optimizations
maturin develop --release
```

#### Building Wheels

To build distributable Python wheels:

```bash
# Build wheel for current platform
maturin build

# Build wheel with release optimizations
maturin build --release

# Install the built wheel
pip install target/wheels/rust_forecast-*.whl
```

## Usage

### Python Example

```python
import rust_forecast

# Make a prediction
input_data = [1.0, 2.0, 3.0]
predictions = rust_forecast.predict(input_data)
print(predictions)  # Output: [1.0, 2.0, 3.0]
```

### Rust Example

```rust
use rust_forecast::predict;

fn main() {
    let input = vec![1.0, 2.0, 3.0];
    match predict(input) {
        Ok(predictions) => println!("Predictions: {:?}", predictions),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

## Testing Python Integration

Run the Python integration tests:

```bash
# First, install in development mode
maturin develop

# Then run the Python tests
python -m pytest rust_forecast/tests_py/

# Or test import directly
python -c "import rust_forecast; print(rust_forecast.predict([1.0, 2.0, 3.0]))"
```

## API Reference

### `predict(input: Vec<f64>) -> Result<Vec<f64>, String>`

Core Rust function that performs prediction.

**Parameters:**
- `input`: A vector of f64 values

**Returns:**
- `Ok(Vec<f64>)`: Predicted values
- `Err(String)`: Error message if input is invalid (e.g., empty vector)

### `predict_py(py_input: Vec<f64>) -> PyResult<Vec<f64>>`

Python-facing wrapper around the core predict function.

**Parameters:**
- `py_input`: A list of float values

**Returns:**
- A list of predicted float values

**Raises:**
- `ValueError`: If input is empty

## Development

### Project Structure

```
rust_forecast/
├── Cargo.toml           # Rust package configuration
├── pyproject.toml       # Python package configuration
├── README.md            # This file
├── src/
│   └── lib.rs          # Main library code with Rust and Python bindings
└── tests_py/
    └── test_import.py  # Python integration tests
```

### Running All Tests

```bash
# Rust tests
cargo test

# Python tests (after maturin develop)
maturin develop && python -m pytest tests_py/
```

## References

This implementation addresses issues referenced in:
- FabianoDicheti/dqtimes#40
- FabianoDicheti/dqtimes#41

## License

See repository root for license information.
