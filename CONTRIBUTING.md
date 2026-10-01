# Contributing to uncloak

Thank you for your interest in contributing!

## Development Setup
```bash
git clone https://github.com/yourusername/uncloak.git
cd uncloak
pip install -e .[dev]
playwright install chromium
pre-commit install
```

## TDD Workflow
We strictly follow Test-Driven Development (TDD):
1. **Red**: Write a failing test for the new feature or bug fix.
2. **Green**: Write the minimum code necessary to make the test pass.
3. **Refactor**: Clean up the code and ensure all tests still pass.

## Code Style
- We use `ruff` for linting and formatting.
- We use `mypy` (strict mode) for type checking.
- Pre-commit hooks will automatically format and check your code before you commit.

## Pull Request Process
1. Ensure all tests pass (`pytest`).
2. Ensure linters pass (`ruff check src/`, `mypy src/uncloak/`).
3. Submit a PR. All CI checks must be green before merging.
