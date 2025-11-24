use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

/// Core prediction logic (can be tested without Python runtime)
fn predict_static_impl(data: &[f64], horizon: usize) -> Result<Vec<f64>, String> {
    // Validate input
    if data.is_empty() {
        return Err("Input data cannot be empty".to_string());
    }
    
    if horizon == 0 {
        return Err("Horizon must be greater than 0".to_string());
    }
    
    // Mock prediction: repeat the last value for the specified horizon
    let last_value = data.last().unwrap();
    let predictions = vec![*last_value; horizon];
    
    Ok(predictions)
}

/// Predict future values based on historical data (mock implementation).
/// 
/// This is a simple mock implementation that returns the last value repeated
/// for the specified horizon. In a production system, this would contain
/// actual forecasting logic.
///
/// # Arguments
///
/// * `data` - Historical data as a vector of floats
/// * `horizon` - Number of future values to predict
///
/// # Returns
///
/// Vector of predicted values (mock: repeats last value)
///
/// # Errors
///
/// Returns PyValueError if:
/// * data is empty
/// * horizon is 0
///
/// # Examples
///
/// ```python
/// import sa_native
/// # Predict 3 future values based on historical data
/// result = sa_native.predict_static([1.0, 2.0, 3.0], 3)
/// # Returns [3.0, 3.0, 3.0] (last value repeated)
/// ```
#[pyfunction]
fn predict_static(data: Vec<f64>, horizon: usize) -> PyResult<Vec<f64>> {
    predict_static_impl(&data, horizon)
        .map_err(|e| PyValueError::new_err(e))
}

/// Python module for time series prediction.
/// 
/// This module provides Rust-based functions for time series forecasting
/// that can be called from Python.
#[pymodule]
fn sa_native(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(predict_static, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_predict_static_valid_input() {
        // Test with valid input
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let horizon = 3;
        let result = predict_static_impl(&data, horizon);
        
        assert!(result.is_ok());
        let predictions = result.unwrap();
        assert_eq!(predictions.len(), 3);
        assert_eq!(predictions, vec![5.0, 5.0, 5.0]);
    }

    #[test]
    fn test_predict_static_single_value() {
        // Test with single value
        let data = vec![42.0];
        let horizon = 5;
        let result = predict_static_impl(&data, horizon);
        
        assert!(result.is_ok());
        let predictions = result.unwrap();
        assert_eq!(predictions.len(), 5);
        assert_eq!(predictions, vec![42.0, 42.0, 42.0, 42.0, 42.0]);
    }

    #[test]
    fn test_predict_static_empty_data() {
        // Test with empty data - should return error
        let data = vec![];
        let horizon = 3;
        let result = predict_static_impl(&data, horizon);
        
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Input data cannot be empty");
    }

    #[test]
    fn test_predict_static_zero_horizon() {
        // Test with zero horizon - should return error
        let data = vec![1.0, 2.0, 3.0];
        let horizon = 0;
        let result = predict_static_impl(&data, horizon);
        
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Horizon must be greater than 0");
    }

    #[test]
    fn test_predict_static_large_horizon() {
        // Test with large horizon
        let data = vec![10.0, 20.0, 30.0];
        let horizon = 100;
        let result = predict_static_impl(&data, horizon);
        
        assert!(result.is_ok());
        let predictions = result.unwrap();
        assert_eq!(predictions.len(), 100);
        // All values should be 30.0 (last value)
        assert!(predictions.iter().all(|&x| x == 30.0));
    }
}
