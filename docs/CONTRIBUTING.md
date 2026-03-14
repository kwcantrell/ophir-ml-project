# Contributing to Ophir ML Project

Thank you for your interest in contributing! This guide outlines the development workflow, code style, and pull request process.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Checklist](#release-checklist)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.10 or higher
- `uv` package manager
- Git installed
- Basic knowledge of PyTorch and machine learning

### Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-org/ophir-ml-project.git
cd ophir-ml-project
```

2. **Create and activate virtual environment**

```bash
# Using uv
uv venv
source .venv/bin/activate  # On Linux/macOS
# or
\.venv\Scripts\activate    # On Windows

# Using pip and venv
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
\.venv\Scripts\activate    # On Windows
```

3. **Install dependencies**

```bash
uv sync
```

4. **Install pre-commit hooks**

```bash
pre-commit install
```

5. **Run tests to verify setup**

```bash
pytest
```

---

## Development Workflow

### Branching Strategy

We use a standard GitFlow-inspired branching model:

- `main`: Production-ready code
- `feature/*`: New features or substantial changes
- `bugfix/*`: Bug fixes for released versions
- `release/*`: Preparation for releases

### Creating a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Good branch names:
# - feature/add-new-metric
# - fix/model-training-issue
# - docs/update-README
```

### Making Changes

1. **Make your changes** to the codebase
2. **Run the linter** to ensure code style compliance

```bash
ruff check .
ruff format .
```

3. **Run tests** to ensure nothing broke

```bash
pytest
pytest --cov=src
```

4. **Run type checking**

```bash
mypy src
```

5. **Commit your changes**

```bash
git add .
git commit -m "feat: add new feature description"
```

See [Git Commit Message Convention](#git-commit-message-convention) below for details.

### Pull Request Process

1. **Push your branch** to GitHub

```bash
git push origin feature/your-feature-name
```

2. **Create a Pull Request (PR)** on GitHub

3. **Wait for automated checks** to pass (CI/CD will run automatically)

4. **Address feedback** from maintainers

5. **Merge** once approved

---

## Code Style Guidelines

### Code Formatting

We use **Black** (via `ruff`) for consistent code formatting:

- **Line length**: 100 characters
- **String quotes**: Double quotes
- **Docstring style**: Google-style
- **Import sorting**: Third-party, first-party, local

### Linting

We use **Ruff** for linting:

- **Formatting**: Handles Black formatting rules
- **Linting**: Follows industry standard rules
- **Security**: Comprehensive security checks enabled
- **Performance**: Performance rule checks enabled

Run linting:

```bash
ruff check .
```

Fix linting issues:

```bash
ruff check . --fix
```

### Type Checking

We use **mypy** for static type checking:

- Enable `disallow_untyped_defs` for core modules
- Relax rules for PyTorch ecosystem libraries
- Run type checking with: `mypy src`

### Docstrings

We use **Google-style docstrings**:

```python
def function_name(param1: int, param2: str) -> bool:
    """Brief description of what the function does.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is negative.
    """
    ...
```

### Documentation

All public APIs should have:

- Brief description in docstring
- Parameter descriptions
- Return type and description
- Example usage (for complex functions)

---

## Git Commit Message Convention

We follow **Conventional Commits** for commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### Commit Scope

Specify the scope to indicate what part of the codebase is affected:

```
feat(models): add new layer class
fix(utils): resolve memory leak issue
docs(README): update installation instructions
```

### Example Commit

```
feat(models): add BatchNorm2d wrapper

- Add BatchNorm2d class to models/batch_norm.py
- Include forward and backward pass implementations
- Add docstrings and type annotations
- Add unit tests for new class

Closes #123
```

### Footer

- Use `Closes #issue-number` to reference issues
- Use `Refs #issue-number` for related issues
- Add breaking change notes if applicable

---

## Pull Request Process

### PR Requirements

All PRs must:

1. **Pass CI/CD checks**: Linting, testing, and type checking
2. **Maintain coverage**: Minimum 80% coverage requirement
3. **Include tests**: New features must have tests
4. **Update documentation**: README and docstrings as needed

### PR Template

Every PR should include:

```markdown
## Description

Brief description of the changes and why they were made.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing

- [ ] I have added tests
- [ ] I have verified the changes work correctly
- [ ] Coverage requirements are met

## Checklist

- [ ] My code follows the project's code style
- [ ] I have added docstrings to public APIs
- [ ] I have updated documentation as needed
- [ ] I have run `ruff` and `mypy` locally
- [ ] All CI/CD checks pass
```

### Review Process

1. **Self-review**: Review your own code before submitting
2. **Request review**: Assign at least one maintainer
3. **Address feedback**: Make requested changes
4. **Squash commits**: Rebase to have clean commit history

---

## Release Checklist

### Pre-Release

Before each release:

1. **Update CHANGELOG.md**

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- Description of changes

### Fixed
- Description of bug fixes
```

2. **Update version** in `pyproject.toml`

3. **Update docs/README.md** with release notes

4. **Run full test suite**:

```bash
pytest
pytest --cov=src --cov-report=term-missing
```

5. **Verify CI/CD**: Ensure all checks pass

### Release Steps

1. Create release branch: `git checkout -b release/v0.x.y`
2. Update version and changelog
3. Create test release package
4. Push release branch
5. Merge release branch to main
6. Create GitHub release
7. Publish package to PyPI

### Post-Release

1. Create new development branch from main
2. Update CHANGELOG.md for next release
3. Announce release on relevant channels

---

## Code of Conduct

### Be Respectful

- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Professional

- Adhere to the [Python Community Code of Conduct](https://www.python.org/psf/conduct/)
- Report issues through appropriate channels
- Remember that we are a global, diverse community

---

## Questions?

If you have questions:

1. **Open an issue**: For questions or feedback
2. **Check existing issues**: Your question might already be answered
3. **Join our community**: [Link to community channels]

---

## License

By contributing to the Ophir ML Project, you agree that your contributions will be licensed under the project's license.

Thank you for contributing! 🎉

## Development Workflow

### Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/kwcantrell/ophir-ml-project.git
cd ophir-ml-project

# Create and activate virtual environment
uv venv .venv && source .venv/bin/activate

# Install dependencies
uv sync

# Install pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Running Tests Locally

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

### Making Changes

1. **Create a feature branch**: `git checkout -b feature/my-feature`
2. **Make your changes** following the code style guidelines
3. **Run tests** to ensure everything passes
4. **Run pre-commit hooks** before committing: `pre-commit run --all-files`
5. **Push your branch** and create a pull request

## Code Style Guidelines

### Ruff Configuration

This project uses Ruff for linting and formatting. Always run:

```bash
uv run ruff check . --fix
uv run ruff format .
```

### Type Annotations

- Use type hints for all function arguments and return values
- Import types from `typing` module: `from typing import Optional, List, Dict`
- Use `@overload` for functions with multiple return types
- Prefer `Literal` for enum-like values

### Docstrings

Use Google-style docstrings for all public APIs:

```python
def my_function(arg: int) -> str:
    """Do something useful.

    Args:
        arg: The input argument.

    Returns:
        The result as a string.
    """
```

### PyTorch Best Practices

```python
# Use context managers for model state
model.train()
# ... training code ...
model.eval()

# Use torch.no_grad() for inference
with torch.no_grad():
    output = model(input)
```

## Pull Request Process

### PR Title Format

```
feat: Add new feature for X
fix: Resolve bug in Y
docs: Update documentation for Z
refactor: Restructure W module
test: Add tests for V
chore: Update configuration
```

### PR Checklist

- [ ] All tests pass (`uv run pytest tests/ -v`)
- [ ] No linting errors (`uv run ruff check .`)
- [ ] No formatting issues (`uv run ruff format .`)
- [ ] Type checking passes (`uv run mypy src/ models/`)
- [ ] Changes are backward compatible (or documented as breaking)
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventional commits

### PR Review Process

1. **Self-review**: Review your own code before submitting
2. **Request review**: Assign maintainers for review
3. **Address feedback**: Make requested changes
4. **Squash commits**: Combine related commits into logical units
5. **Merge**: Maintainer merges after approval

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build process or auxiliary tool changes

### Example Commits

```
feat(train): Add mixed precision training support

feat(eval): Implement evaluation pipeline

fix(seeds): Fix seed setting order for reproducibility
```

## Release Checklist

Before releasing a new version:

- [ ] Update `CHANGELOG.md`
- [ ] Increment version in `pyproject.toml`
- [ ] Run tests on all platforms
- [ ] Create release notes
- [ ] Tag the release: `git tag v1.0.0 && git push --tags`

## Code of Conduct

- Be respectful and inclusive
- Focus on what's best for the project
- Assume good intentions
- Welcome newcomers

## Questions?

- Open an [issue](https://github.com/kwcantrell/ophir-ml-project/issues)
- Check the [documentation](https://github.com/kwcantrell/ophir-ml-project/tree/main/docs)
- Join the [Discussions](https://github.com/kwcantrell/ophir-ml-project/discussions)
