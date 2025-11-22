use pyo3::prelude::*;

/// Core Rust prediction function
/// This is a mock implementation that multiplies the input by 1.0 (returns the same values)
pub fn predict(input: Vec<f64>) -> Result<Vec<f64>, String> {
    if input.is_empty() {
        return Err("Input vector cannot be empty".to_string());
    }
    
    // Mock prediction: multiply by 1.0 (return the same values)
    Ok(input.iter().map(|&x| x * 1.0).collect())
}

/// Python-facing prediction function with PyO3 bindings
/// 
/// # Arguments
/// * `py_input` - A vector of f64 values to predict on
/// 
/// # Returns
/// * A vector of f64 predictions
/// 
/// # Example
/// ```python
/// import rust_forecast
/// result = rust_forecast.predict([1.0, 2.0, 3.0])
/// print(result)  # [1.0, 2.0, 3.0]
/// ```
#[pyfunction(name = "predict")]
fn predict_py(py_input: Vec<f64>) -> PyResult<Vec<f64>> {
    predict(py_input)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e))
}

/// Python module definition
#[pymodule]
fn rust_forecast(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(predict_py, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_predict_valid_input() {
        let input = vec![1.0, 2.0, 3.0];
        let result = predict(input.clone());
        
        assert!(result.is_ok());
        let output = result.unwrap();
        assert_eq!(output.len(), 3);
        assert_eq!(output, vec![1.0, 2.0, 3.0]);
    }

    #[test]
    fn test_predict_empty_input() {
        let input: Vec<f64> = vec![];
        let result = predict(input);
        
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Input vector cannot be empty");
    }

    #[test]
    fn test_predict_with_negative_values() {
        let input = vec![-1.0, -2.0, -3.0];
        let result = predict(input.clone());
        
        assert!(result.is_ok());
        let output = result.unwrap();
        assert_eq!(output, vec![-1.0, -2.0, -3.0]);
    }

    #[test]
    fn test_predict_with_zeros() {
        let input = vec![0.0, 0.0, 0.0];
        let result = predict(input.clone());
        
        assert!(result.is_ok());
        let output = result.unwrap();
        assert_eq!(output, vec![0.0, 0.0, 0.0]);
    }
}
