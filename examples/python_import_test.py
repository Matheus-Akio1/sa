#!/usr/bin/env python3
"""
Python Import Test for sa_native Rust Library

This script demonstrates how to build and test the sa_native library
which provides Rust-based time series prediction functions via Python bindings.

Build Instructions:
    1. Install maturin (if not already installed):
       pip install maturin

    2. Build and install the library in development mode:
       cd rust/sa_native
       maturin develop --release

    3. Run this test script:
       python examples/python_import_test.py

Alternative Build Method:
    Build a wheel package:
       cd rust/sa_native
       maturin build --release
       pip install target/wheels/sa_native-*.whl
"""

def test_import():
    """Test basic import of the sa_native module."""
    try:
        import sa_native
        print("✓ Module 'sa_native' imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import sa_native: {e}")
        print("\nPlease build the library first:")
        print("  cd rust/sa_native")
        print("  pip install maturin")
        print("  maturin develop --release")
        return False


def test_predict_static():
    """Test the predict_static function with various inputs."""
    import sa_native
    
    print("\n--- Testing predict_static function ---")
    
    # Test 1: Basic prediction
    print("\nTest 1: Basic prediction")
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    horizon = 3
    result = sa_native.predict_static(data, horizon)
    print(f"Input: {data}, Horizon: {horizon}")
    print(f"Result: {result}")
    assert result == [5.0, 5.0, 5.0], f"Expected [5.0, 5.0, 5.0], got {result}"
    print("✓ Test passed")
    
    # Test 2: Single value prediction
    print("\nTest 2: Single value prediction")
    data = [42.0]
    horizon = 2
    result = sa_native.predict_static(data, horizon)
    print(f"Input: {data}, Horizon: {horizon}")
    print(f"Result: {result}")
    assert result == [42.0, 42.0], f"Expected [42.0, 42.0], got {result}"
    print("✓ Test passed")
    
    # Test 3: Larger horizon
    print("\nTest 3: Larger horizon")
    data = [10.0, 20.0, 30.0]
    horizon = 5
    result = sa_native.predict_static(data, horizon)
    print(f"Input: {data}, Horizon: {horizon}")
    print(f"Result: {result}")
    assert result == [30.0] * 5, f"Expected {[30.0] * 5}, got {result}"
    print("✓ Test passed")
    
    # Test 4: Error handling - empty data
    print("\nTest 4: Error handling - empty data")
    try:
        result = sa_native.predict_static([], 3)
        print("✗ Should have raised an error for empty data")
        return False
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    
    # Test 5: Error handling - zero horizon
    print("\nTest 5: Error handling - zero horizon")
    try:
        result = sa_native.predict_static([1.0, 2.0], 0)
        print("✗ Should have raised an error for zero horizon")
        return False
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    
    return True


def main():
    """Main test runner."""
    print("=" * 60)
    print("sa_native - Python Import and Functionality Test")
    print("=" * 60)
    
    # Test import
    if not test_import():
        return 1
    
    # Test functionality
    try:
        if not test_predict_static():
            return 1
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 60)
    print("All tests passed successfully! ✓")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
