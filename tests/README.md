# Testing Guide

## Overview

This repository includes a comprehensive test suite for the PyTorch ML project.

## Table of Contents

- [Test Structure](#test-structure)
- [Writing Tests](#writing-tests)
- [Running Test Suites](#running-test-suites)
- [Mocking PyTorch Components](#mocking-pytorch-components)
- [Coverage Reporting](#coverage-reporting)
- [Best Practices](#best-practices)

---

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures and configurations
├── README.md                      # This file
├── unit/                          # Unit tests for individual components
│   ├── test_model.py             # Model architecture and forward pass
│   ├── test_layers.py            # Individual layer implementations
│   ├── test_utils.py             # Utility functions
│   ├── test_training.py          # Training loop and optimizers
│   ├── test_metrics.py           # Metric calculations
│   ├── test_seeds.py             # Reproducibility checks
│   └── test_data_loading.py      # Data loading pipelines
├── integration/                   # Integration tests
│   ├── test_training_pipeline.py # Full training workflow
│   └── test_evaluation_pipeline.py # Evaluation workflow
├── e2e/                           # End-to-end tests
│   └── test_full_workflow.py     # Complete application workflow
├── benchmark/                     # Performance tests
│   └── test_performance.py       # Speed and resource benchmarks
└── fixtures/                      # Test fixtures and mock data
    └── sample_data.py            # Mock datasets and utilities
```

## Running Test Suites

### Basic Test Run

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run with parallel execution
pytest -n auto --dist=loadfile

# Run specific test file
pytest tests/unit/test_model.py

# Run specific test function
pytest tests/unit/test_model.py::TestModel::test_forward_pass
```

### Parallel Execution

```bash
# Run tests in parallel (faster execution)
pytest -n auto --dist=loadfile

# Run with coverage and parallel execution
pytest -n auto --cov=src --cov-report=html:coverage.html
```

### Test Discovery

Pytest automatically discovers tests with these naming patterns:

- **Files**: `test_*.py`, `*_test.py`
- **Functions**: `test_*`
- **Classes**: `Test*`, `*Test`

### Configuration

Pytest options are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-ra -q --cov=src --cov-report=term-missing"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*", "*Test"]
python_functions = ["test_*"]
xfail_strict = true  # Strict xfail for better error messages
```

---

## Writing Tests

### Basic Test Structure

```python
"""Test for model training utilities."""

import numpy as np
import pytest
import torch
from src.utils.training import calculate_loss, train_step

@pytest.fixture
def sample_data():
    """Create sample data for tests."""
    return {
        'input': torch.randn(4, 10, 10),
        'target': torch.randint(0, 2, (4, 10, 10)),
    }

def test_calculate_loss(sample_data):
    """Test loss calculation."""
    loss = calculate_loss(sample_data['input'], sample_data['target'])
    assert isinstance(loss, torch.Tensor)
    assert loss.shape == torch.Size([])
```

### Test Naming Conventions

- All test functions should start with `test_`
- Test names should describe what is being tested
- Use plural nouns for multiple items being tested

```python
def test_compute_accuracy_with_batch_size_32():
    """Test accuracy computation with batch size 32."""
    ...
```

### Writing Good Tests

- **Test behavior, not implementation**: Test what the code does, not how it does it
- **Use descriptive names**: Test names should explain what is being tested
- **Single responsibility**: Each test should verify one behavior
- **Fast execution**: Keep tests fast for better developer experience

### Example: Well-Structured Test File

```python
"""Tests for model training."""

import numpy as np
import pytest
import torch
from src.utils.training import train_step, calculate_loss

@pytest.fixture
def model():
    """Create model fixture."""
    return torch.nn.Sequential(
        torch.nn.Linear(28 * 28, 128),
        torch.nn.ReLU(),
        torch.nn.Linear(128, 10),
    )

@pytest.fixture
def dataset():
    """Create dataset fixture."""
    X = torch.randn(1000, 28 * 28)
    y = torch.randint(0, 10, (1000,))
    return torch.utils.data.TensorDataset(X, y)

class TestTrainingStep:
    """Test training step functionality."""

    def test_training_step_returns_loss(self, model, dataset):
        """Test that training step returns a loss value."""
        loader = torch.utils.data.DataLoader(dataset, batch_size=32)
        output, loss = train_step(model, loader, loss_fn=torch.nn.CrossEntropyLoss())

        assert isinstance(loss, torch.Tensor)
        assert loss.item() > 0

    def test_training_step_updates_parameters(self, model, dataset):
        """Test that training step updates model parameters."""
        optimizer = torch.optim.Adam(model.parameters())
        loader = torch.utils.data.DataLoader(dataset, batch_size=32)

        # Capture initial parameters
        initial_params = {name: param.clone() for name, param in model.named_parameters()}

        # Run training step
        output, loss = train_step(model, loader, loss_fn=torch.nn.CrossEntropyLoss())
        optimizer.step()

        # Check parameters changed
        changed_params = sum(
            1 for name, param in model.named_parameters()
            if not torch.equal(param, initial_params[name])
        )
        assert changed_params > 0
```

### Testing Edge Cases

```python
def test_empty_input_handling():
    """Test that empty input is handled gracefully."""
    with pytest.raises(ValueError, match="empty input"):
        process_empty_tensor(torch.empty(0, 10))

def test_large_batch_handling():
    """Test handling of large batch sizes."""
    large_batch = torch.randn(10000, 10)
    result = process_tensor(large_batch)
    assert result.shape == large_batch.shape
```

### Performance Tests

```python
# tests/benchmark/test_performance.py

import pytest
import time
import torch

@pytest.mark.benchmark
def test_forward_pass_benchmark():
    """Benchmark forward pass performance."""
    model = torch.nn.Linear(1000, 10)
    x = torch.randn(100, 1000)

    start = time.time()
    for _ in range(100):
        _ = model(x)
    elapsed = time.time() - start

    # Check performance is within acceptable range
    assert elapsed < 1.0  # Should complete in under 1 second
```

---

## Mocking PyTorch Components

### Mocking Model Inputs

```python
from unittest.mock import patch, MagicMock
import torch
import torch.nn as nn

def test_model_with_mocked_forward():
    """Test model with mocked forward pass."""
    model = nn.Linear(10, 2)

    # Mock the forward method
    with patch.object(model, 'forward', return_value=torch.randn(4, 2)) as mock_forward:
        output = model(torch.randn(4, 10))

        # Verify mock was called
        mock_forward.assert_called_once()

        # Verify output shape
        assert output.shape == (4, 2)
```

### Mocking Tensor Computations

```python
from unittest.mock import patch
import torch

def test_loss_with_mocked_computation():
    """Test loss function with mocked tensor computation."""
    model_output = torch.randn(4, 10)
    target = torch.randint(0, 2, (4, 10, 10))

    # Mock the loss computation
    with patch('src.models.compute_loss', return_value=torch.tensor(0.5)):
        loss = compute_loss(model_output, target)

        assert loss == 0.5
```

### Mocking External APIs

```python
import pytest
from unittest.mock import patch
import requests

def test_with_mocked_api_call():
    """Test with mocked API call to avoid network requests."""

    mock_response = {
        'status': 'success',
        'data': {'result': 'mocked_value'}
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Your code that makes the API call
        response = make_api_call()

        # Verify mock was called correctly
        mock_get.assert_called_once()
```

### Creating Mock Data Generators

```python
# tests/fixtures/sample_data.py

import numpy as np
import torch

def generate_mnist_batch(batch_size: int = 32) -> tuple[torch.Tensor, torch.Tensor]:
    """Generate MNIST-style batch for testing."""
    X = torch.randn(batch_size, 1, 28, 28)
    y = torch.randint(0, 10, (batch_size,))
    return X, y

def generate_cifar_batch(batch_size: int = 32) -> tuple[torch.Tensor, torch.Tensor]:
    """Generate CIFAR-style batch for testing."""
    X = torch.randn(batch_size, 3, 32, 32)
    y = torch.randint(0, 10, (batch_size,))
    return X, y

def create_mock_dataset(num_samples: int = 1000) -> torch.utils.data.Dataset:
    """Create a simple mock dataset for testing."""
    class MockDataset(torch.utils.data.Dataset):
        def __init__(self, num_samples):
            self.data = torch.randn(num_samples, 10)
            self.labels = torch.randint(0, 5, num_samples)

        def __len__(self) -> int:
            return len(self.data)

        def __getitem__(self, idx: int):
            return self.data[idx], self.labels[idx]

    return MockDataset(num_samples)
```

---

## Coverage Reporting

### View Coverage Report

```bash
# Terminal report with missing coverage
pytest --cov=src --cov-report=term-missing

# HTML report for browser viewing
pytest --cov=src --cov-report=html:coverage.html

# XML report for CI/CD
pytest --cov=src --cov-report=xml:coverage.xml

# Coverage for specific module
pytest --cov=src.models --cov-report=term-missing
```

### Coverage Thresholds

Coverage configuration in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "no cov",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

### Minimum Coverage Requirements

- **Overall coverage**: Minimum 80%
- **Core modules**: Minimum 85%
- **Utility modules**: Minimum 75%

---

## Best Practices

### Test Organization

1. **Group related tests**: Keep tests for the same feature in the same file
2. **Use fixtures**: Leverage pytest fixtures for setup/teardown
3. **Keep tests independent**: Each test should be runnable in isolation
4. **Test at the right level**: Unit tests for functions, integration tests for components

### Writing Good Tests

- **Test behavior, not implementation**: Test what the code does, not how it does it
- **Use descriptive names**: Test names should explain what is being tested
- **Single responsibility**: Each test should verify one behavior
- **Fast execution**: Keep tests fast for better developer experience

### Example with PyTorch Models

```python
import pytest
import torch
from src.models import ResNet18


@pytest.fixture
def model():
    """Create a ResNet18 model."""
    return ResNet18()


def test_model_output_shape(model):
    """Test that model outputs have expected shape."""
    x = torch.randn(1, 3, 224, 224)
    y = model(x)
    assert y.shape == (1, 1000)
```

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:

- Push to main branch
- Pull request creation
- Pull request updates

### Coverage Badge

```markdown
[![Coverage](https://codecov.io/gh/your-org/your-repo/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/your-repo)
```

---

## Contributing

When adding new tests:

1. Create tests in the appropriate directory
2. Add tests to CI configuration if needed
3. Ensure coverage requirements are met
4. Add fixtures if shared across tests

Thank you for contributing to the Ophir ML Project testing infrastructure!

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_training.py -v

# Run tests with warnings
uv run pytest tests/ -v -W error
```

### CI Tests

Tests run with additional options in CI:

```bash
uv run pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing
```

## Writing Tests

### Best Practices

1. **Test at the function/class level**: Keep tests focused and atomic
2. **Use fixtures**: Leverage `conftest.py` for shared setup
3. **Mock external dependencies**: Use `unittest.mock` for PyTorch objects
4. **Test both success and failure cases**: Include edge cases
5. **Keep tests independent**: Avoid state leakage between tests

### Example Unit Test

```python
import pytest
from src.utils import set_seeds


def test_determinism():
    """Verify that set_seeds makes training reproducible."""
    set_seeds(seed=42)
    # Test code here...
```

### Example with PyTorch Models

```python
import pytest
import torch
from src.models import ResNet18


@pytest.fixture
def model():
    """Create a ResNet18 model."""
    return ResNet18()


def test_model_output_shape(model):
    """Test that model outputs have expected shape."""
    x = torch.randn(1, 3, 224, 224)
    y = model(x)
    assert y.shape == (1, 1000)
```

## Mocking PyTorch Components

```python
from unittest.mock import patch, MagicMock
import torch.nn as nn


@patch("src.train.main.nn.Module.train")
def test_train_epoch_without_training(mock_train):
    """Test train_epoch without actual training."""
    # Setup mocks
    model = MagicMock(spec=nn.Module)
    # ...
```

## Coverage Requirements

- Minimum coverage: **80%**
- Core modules: **90%**
- Models: **70%** (due to third-party dependencies)

## Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
python_functions = "test_*"
addopts = "-v --strict-markers"
xfail_strict = true
```
