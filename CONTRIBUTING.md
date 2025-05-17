# Contributing to Product Information Extractor

Thank you for your interest in contributing to Product Information Extractor! This document provides guidelines for contributing to the project.

## Code of Conduct

Please note that this project follows a Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

1. Check the issue tracker to ensure the bug hasn't already been reported
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce the issue
   - Expected behavior vs actual behavior
   - System information (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Enhancements

1. Check the issue tracker for similar suggestions
2. Create a new issue with the `enhancement` label
3. Provide a clear description of the proposed feature
4. Include use cases and potential implementation ideas

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest tests/`)
6. Format code with Black (`black .`)
7. Sort imports with isort (`isort .`)
8. Run linting (`flake8 .`)
9. Run type checking (`mypy .`)
10. Commit changes (`git commit -m 'Add amazing feature'`)
11. Push to branch (`git push origin feature/amazing-feature`)
12. Create a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/Product-Information-Extractor.git
cd Product-Information-Extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Code Style Guidelines

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use isort for import sorting
- Add type hints to all functions
- Write descriptive variable names
- Include docstrings for all functions and classes
- Keep functions focused and small
- Write comprehensive tests

### Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Use pytest for testing
- Include both unit and integration tests
- Test edge cases and error conditions

### Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update configuration documentation
- Include examples where appropriate

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally

Example:
```
Add batch processing functionality

- Implement batch image processing
- Add progress tracking
- Update UI to support batch mode
- Add tests for batch processing

Fixes #123
```

### Pre-commit Checklist

Before submitting a PR, ensure:

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] No linting errors
- [ ] Type hints are added
- [ ] Documentation is updated
- [ ] Commit messages follow guidelines

Thank you for contributing!