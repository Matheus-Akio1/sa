"""
Python integration tests for rust_forecast module.

These tests validate that the Rust library can be imported and used from Python.
"""

def test_import_module():
    """Test that the rust_forecast module can be imported."""
    try:
        import rust_forecast
        assert rust_forecast is not None
    except ImportError as e:
        raise AssertionError(f"Failed to import rust_forecast: {e}")


def test_predict_function_exists():
    """Test that the predict function exists in the module."""
    import rust_forecast
    assert hasattr(rust_forecast, 'predict') or hasattr(rust_forecast, 'predict_py')


def test_predict_basic_functionality():
    """Test basic predict functionality with valid input."""
    import rust_forecast
    
    # Test with simple input
    input_data = [1.0, 2.0, 3.0]
    
    # Try both possible function names
    if hasattr(rust_forecast, 'predict'):
        result = rust_forecast.predict(input_data)
    else:
        result = rust_forecast.predict_py(input_data)
    
    # Validate result type and value
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) == 3, f"Expected length 3, got {len(result)}"
    
    # For mock implementation (multiply by 1.0), output should equal input
    assert result == [1.0, 2.0, 3.0], f"Expected [1.0, 2.0, 3.0], got {result}"


def test_predict_with_different_values():
    """Test predict with various input values."""
    import rust_forecast
    
    test_cases = [
        ([5.0, 10.0, 15.0], [5.0, 10.0, 15.0]),
        ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
        ([-1.0, -2.0, -3.0], [-1.0, -2.0, -3.0]),
        ([100.5], [100.5]),
    ]
    
    for input_data, expected in test_cases:
        if hasattr(rust_forecast, 'predict'):
            result = rust_forecast.predict(input_data)
        else:
            result = rust_forecast.predict_py(input_data)
        
        assert result == expected, f"For input {input_data}, expected {expected}, got {result}"


def test_predict_empty_input_raises_error():
    """Test that empty input raises an appropriate error."""
    import rust_forecast
    
    try:
        if hasattr(rust_forecast, 'predict'):
            result = rust_forecast.predict([])
        else:
            result = rust_forecast.predict_py([])
        
        # If we get here, the function didn't raise an error
        raise AssertionError("Expected ValueError for empty input, but no error was raised")
    
    except ValueError as e:
        # This is expected
        assert "empty" in str(e).lower(), f"Error message should mention 'empty', got: {e}"
    
    except Exception as e:
        # Some other error occurred
        raise AssertionError(f"Expected ValueError, got {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Run tests manually if executed directly
    print("Running test_import_module...")
    test_import_module()
    print("✓ Passed")
    
    print("Running test_predict_function_exists...")
    test_predict_function_exists()
    print("✓ Passed")
    
    print("Running test_predict_basic_functionality...")
    test_predict_basic_functionality()
    print("✓ Passed")
    
    print("Running test_predict_with_different_values...")
    test_predict_with_different_values()
    print("✓ Passed")
    
    print("Running test_predict_empty_input_raises_error...")
    test_predict_empty_input_raises_error()
    print("✓ Passed")
    
    print("\nAll tests passed!")
