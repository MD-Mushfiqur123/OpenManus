# Contributing to OpenManus

We love your input! We want to make contributing to OpenManus as easy and transparent as possible.

## Development Setup

### Prerequisites

- Python 3.11 or 3.12
- Git
- Docker (optional, for sandbox testing)

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/OpenManus.git
cd OpenManus

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov

# Copy config
cp config/config.example.toml config/config.toml
# Edit config/config.toml with your API keys
```

### Configuration

1. Copy `config/config.example.toml` to `config/config.toml`
2. Add your LLM API keys
3. See `config/` for provider-specific templates

## Code Style

- Follow PEP 8
- Use type hints for all function signatures
- No commented-out code in commits
- Use meaningful variable names
- Keep functions focused and small

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run tests: `pytest tests/ -x --tb=short`
4. Run linting: `pre-commit run --all-files`
5. Commit with conventional commit message
6. Push and create PR

## Conventional Commits

```
feat: new feature
fix: bug fix
docs: documentation changes
test: adding or updating tests
refactor: code restructuring
perf: performance improvement
security: security hardening
ci: CI/CD changes
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -x --tb=short

# Run specific test file
pytest tests/test_schema.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing
```

### Writing Tests

- Place tests in `tests/test_<module>.py` or `tests/test_<module>/`
- Use pytest-asyncio for async tests
- Use mocks from `tests/mocks/` for external dependencies
- All new features must include tests

## Project Structure

```
OpenManus/
├── app/
│   ├── agent/         # Agent implementations
│   ├── flow/          # Execution flows
│   ├── tool/          # Tool implementations
│   │   └── security/  # Security module
│   ├── config.py      # Configuration
│   ├── llm.py         # LLM integration
│   └── schema.py      # Data models
├── config/            # Configuration files
├── tests/
│   ├── mocks/         # Test mocks
│   └── ...            # Test modules
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## Security

- Report security issues privately (see SECURITY.md)
- Do not commit API keys or secrets
- Input sanitization is handled by `app/tool/security/`
- All tool inputs are validated by default

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and professional

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
