# Contributing to Kipu API Python library

Thank you for your interest in contributing to the Kipu API Python library! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- A GitHub account

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/Rahulkumar010/kipu-python.git
   cd kipu-python
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   
   **Traditional (pip)**:
   ```bash
   pip install -e ".[dev]"
   ```
   
   **Fast (UV - recommended)**: 10x faster!
   ```bash
   pip install uv
   uv pip install -e ".[dev]"
   ```
   
   Or use Makefile:
   ```bash
   make install-dev
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🧪 Development Workflow

### Code Quality
try maintaining code quality standards:

- **Formatting**: Use `black` for code formatting
- **Import Sorting**: Use `isort` for import organization
- **Linting**: Use `flake8` for code linting
- **Type Checking**: Use `mypy` for static type checking
- **Security**: Use `bandit` and `safety` for security checks

### Running Tests
```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/test_auth.py -v
```

### Code Formatting
```bash
# Format code
make format

# Check formatting
make lint
```

### Type Checking
```bash
make type-check
```

### Security Checks
```bash
make security
```

## 📝 Contribution Guidelines

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Changes**
   - Write clear, concise code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow existing code style

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/amazing-feature
   ```

### Commit Message Guidelines

Use conventional commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or modifications
- `chore:` Maintenance tasks

Examples:
```
feat: add support for new patient endpoint
fix: resolve authentication signature generation issue
docs: update README with new examples
test: add unit tests for flattener module
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions and methods
- Write docstrings for all public functions
- Keep line length under 88 characters
- Use descriptive variable and function names

### Testing Requirements

- All new code must have corresponding tests
- Tests should cover both success and error cases
- Aim for >90% test coverage
- Use descriptive test names
- Mock external API calls in tests

### Documentation

- Update README.md for new features
- Add docstrings to all public functions
- Update CHANGELOG.md
- Include code examples for new functionality

## 🏥 Healthcare Code Guidelines

Since this library handles healthcare data:

### Security Considerations
- Never log sensitive patient data
- Use secure credential handling
- Follow HIPAA compliance guidelines
- Validate all inputs thoroughly

### Data Handling
- Respect PHI (Protected Health Information) guidelines
- Implement proper error handling for sensitive operations
- Use secure HTTP practices
- Follow data minimization principles

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - library version
   - Operating system

2. **Reproduction Steps**
   - Clear steps to reproduce the issue
   - Minimal code example
   - Expected vs actual behavior

3. **Error Details**
   - Full error messages
   - Stack traces
   - Relevant logs

## 💡 Feature Requests

For feature requests:

1. **Check Existing Issues**
   - Search for similar requests
   - Check project roadmap

2. **Provide Context**
   - Use case description
   - Expected functionality
   - Potential implementation approach

3. **Healthcare Context**
   - Explain healthcare-specific requirements
   - Consider compliance implications

## 📋 Development Tasks

### Common Tasks

1. **Adding New Endpoint**
   ```python
   # In client.py
   async def get_new_endpoint(self, params: Optional[Dict[str, Any]] = None,
                             flatten: Optional[bool] = None) -> Union[Dict[str, Any], pd.DataFrame]:
       """Get data from new endpoint"""
       response = await self.get("/api/new_endpoint", params)
       return await self._process_response(response, flatten)
   ```

2. **Adding New Exception**
   ```python
   # In exceptions.py
   class KipuNewError(KipuAPIError):
       """Raised when new specific error occurs"""
       pass
   ```

3. **Adding Tests**
   ```python
   # In tests/test_new_feature.py
   class TestNewFeature:
       def test_new_functionality(self):
           """Test new functionality"""
           # Test implementation
           pass
   ```

### Release Process

1. **Update Version**
   - Update `__version__` in `__init__.py`
   - Update version in `setup.py` and `pyproject.toml`

2. **Update Documentation**
   - Update CHANGELOG.md
   - Update README.md if needed

3. **Create Release**
   - Tag release in Git
   - GitHub Actions will handle PyPI deployment

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and grow
- Maintain professional communication

### Healthcare Context

- Respect patient privacy in all discussions
- Consider compliance implications
- Prioritize security and data protection
- Follow healthcare industry best practices

## ❓ Getting Help

- **Documentation**: Check existing docs and examples
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers at rahul01110100@gmail.com

## 🏆 Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors list
- Project documentation

Thank you for contributing to the Kipu API Python library! 🎉
