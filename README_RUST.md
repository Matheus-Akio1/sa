# Rust Library with Python Bindings (sa_native)

This repository contains a Rust library (`sa_native`) that provides time series prediction functionality with Python bindings via PyO3. This implementation fulfills the requirements from issues #40 and #41 of the FabianoDicheti/dqtimes repository.

## Overview

The `sa_native` library is a Rust-based module that can be imported and used from Python. It provides:
- A `predict_static` function for mock time series forecasting
- Input validation and error handling
- Comprehensive unit tests in Rust
- Python integration tests

## Project Structure

```
rust/sa_native/
├── Cargo.toml              # Rust package configuration
├── pyproject.toml          # Python package metadata
├── src/
│   └── lib.rs             # Main library code with predict_static function
└── target/                # Build artifacts (generated)
    └── wheels/            # Python wheel packages (generated)

examples/
└── python_import_test.py  # Python usage examples and tests
```

## Requirements

- **Rust**: 1.56 or later (with Cargo)
- **Python**: 3.8 or later
- **Maturin**: 0.14 or later (for building Python wheels)

## Building the Library

### Option 1: Build and Install with Maturin (Recommended)

1. Install maturin if you haven't already:
   ```bash
   pip install maturin
   ```

2. Build and create a wheel package:
   ```bash
   cd rust/sa_native
   maturin build --release
   ```

3. Install the generated wheel:
   ```bash
   pip install target/wheels/sa_native-*.whl
   ```

### Option 2: Development Mode (Requires Virtual Environment)

If you're working in a Python virtual environment:

```bash
cd rust/sa_native
maturin develop --release
```

This installs the package in editable mode for development.

## Running Tests

### Rust Unit Tests

Run the Rust unit tests to verify the core logic:

```bash
cd rust/sa_native
cargo test --lib
```

This will run 5 unit tests covering:
- Valid input with expected output
- Single value prediction
- Empty data error handling
- Zero horizon error handling
- Large horizon prediction

### Python Integration Tests

After building and installing the library, run the Python integration tests:

```bash
python examples/python_import_test.py
```

This verifies:
- Module import functionality
- Basic prediction operations
- Error handling from Python
- Input validation

## Usage Example

```python
import sa_native

# Predict 3 future values based on historical data
historical_data = [1.0, 2.0, 3.0, 4.0, 5.0]
horizon = 3
predictions = sa_native.predict_static(historical_data, horizon)
print(predictions)  # Output: [5.0, 5.0, 5.0]
```

### API Documentation

#### `predict_static(data: List[float], horizon: int) -> List[float]`

Predict future values based on historical data using a simple mock implementation.

**Parameters:**
- `data`: Historical data as a list of floats
- `horizon`: Number of future values to predict (must be > 0)

**Returns:**
- List of predicted float values (currently: last value repeated)

**Raises:**
- `ValueError`: If data is empty or horizon is 0

**Note:** This is a mock implementation. In production, this would contain actual forecasting algorithms.

## GitHub Actions CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/rust-python.yml`) that:
1. Runs Rust unit tests (`cargo test`)
2. Builds the Python package with maturin
3. Tests Python import and basic functionality

The workflow runs automatically on:
- Push to `main` branch
- Pull requests to `main` branch

## Development Workflow

1. **Make changes** to `src/lib.rs`
2. **Run Rust tests**: `cargo test --lib`
3. **Build the package**: `maturin build --release`
4. **Install locally**: `pip install target/wheels/sa_native-*.whl --force-reinstall`
5. **Test Python integration**: `python examples/python_import_test.py`
6. **Commit changes** and push to GitHub

## Implementation Details

### Mock Prediction Algorithm

The current implementation uses a simple mock algorithm that repeats the last value in the historical data for the specified horizon. This is intentional for demonstration purposes.

**Example:**
- Input: `[1.0, 2.0, 3.0]`, Horizon: `5`
- Output: `[3.0, 3.0, 3.0, 3.0, 3.0]`

### Architecture

The library separates core logic from Python bindings:
- `predict_static_impl`: Pure Rust function with the core algorithm
- `predict_static`: PyO3-wrapped function exposed to Python
- Unit tests operate on `predict_static_impl` to avoid Python runtime dependency

## Troubleshooting

### Import Error in Python

If you get `ImportError: No module named 'sa_native'`:
1. Ensure you've built the library: `cd rust/sa_native && maturin build --release`
2. Install the wheel: `pip install target/wheels/sa_native-*.whl`

### Maturin Development Mode Error

If `maturin develop` fails with "Couldn't find a virtualenv":
- Either create and activate a Python virtual environment, or
- Use `maturin build` + `pip install <wheel>` instead

### Cargo Test Fails

If you see linking errors when running `cargo test`:
- Use `cargo test --lib` instead of just `cargo test`
- This avoids issues with the PyO3 extension module during testing

## References

- [PyO3 Documentation](https://pyo3.rs/)
- [Maturin Documentation](https://www.maturin.rs/)
- [Issues #40 and #41 from FabianoDicheti/dqtimes](https://github.com/FabianoDicheti/dqtimes/issues/)

## License

This project is part of the Matheus-Akio1/sa repository. See the main repository for license information.
