# Property-Based Tests

This directory contains property-based tests for the wa-leg-mcp project using the Hypothesis library.

## Overview

Property-based tests verify that universal properties hold across all inputs, complementing traditional unit tests that verify specific examples. These tests generate hundreds of random test cases to ensure robustness.

## Running Property Tests

### Run all property tests:
```bash
pytest tests/property/ -v
```

### Run property tests with coverage:
```bash
pytest tests/property/ --cov=wa_leg_mcp
```

### Run only property-marked tests:
```bash
pytest -m property_test
```

### Exclude property tests (for faster CI):
```bash
pytest -m "not property_test"
```

## Test Configuration

- **Minimum iterations**: 100 examples per property test
- **Framework**: Hypothesis 6.0+
- **Test marker**: `@pytest.mark.property_test`

## Current Property Tests

### test_roll_call_response_structure.py

**Feature**: missing-api-coverage  
**Property 1**: Response Structure Consistency

Tests that roll call responses have consistent structure across all valid inputs:

1. **test_response_structure_consistency_with_data**: Verifies response structure when API returns roll call data
2. **test_response_structure_consistency_empty_data**: Verifies response structure when API returns empty results
3. **test_response_structure_consistency_with_error**: Verifies error response structure
4. **test_response_structure_consistency_with_none_return**: Verifies response structure when API returns None

**Validates**: Requirements 1.2

## Writing New Property Tests

When adding new property tests:

1. Use the `@given` decorator with appropriate strategies
2. Set `@settings(max_examples=100)` for minimum 100 iterations
3. Add `@pytest.mark.property_test` marker
4. Include feature and property tags in docstring:
   ```python
   """
   Feature: feature-name, Property N: Property Name
   
   Description of what property is being tested.
   """
   ```
5. Use descriptive test names that explain the property being verified

## Test Strategies

Common Hypothesis strategies used:

- `biennium_strategy`: Generates valid biennium strings (e.g., "2023-24")
- `bill_number_strategy`: Generates valid bill numbers in various formats
- `st.sampled_from()`: Select from a list of valid values
- `st.integers()`: Generate integer values within a range
- `st.builds()`: Construct complex objects from simpler strategies

## Debugging Failed Property Tests

When a property test fails, Hypothesis will:

1. Show the failing example
2. Attempt to shrink it to the minimal failing case
3. Save the example for replay

To replay a failing example:
```python
@given(...)
@example(failing_value_1, failing_value_2)  # Add this line
def test_property(...):
    ...
```

## References

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Property-Based Testing Guide](https://hypothesis.works/articles/what-is-property-based-testing/)
- [Design Document](.kiro/specs/missing-api-coverage/design.md) - See "Correctness Properties" section
