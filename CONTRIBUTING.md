# Contributing to Black Sultan OS

Thank you for considering contributing to Black Sultan OS! This document provides guidelines for contributing to the project.

## Code Organization

The project follows a modular architecture:

- **`src/config/`**: Configuration management
- **`src/models/`**: Database models
- **`src/routes/`**: API endpoints and blueprints
- **`src/services/`**: Business logic and core functionality
- **`src/utils/`**: Utility functions and helpers
- **`src/static/`**: Frontend static files

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Aaronlinke/black-sultan-os-professional.git
cd black-sultan-os-professional
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment configuration:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
cd src
python main.py
```

## Code Style Guidelines

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Organize imports alphabetically within groups:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

## Project Structure Guidelines

- Place business logic in `services/`
- Place API endpoints in `routes/`
- Place utility functions in `utils/`
- Place configuration in `config/`
- Keep models in `models/`

## Testing

Before submitting a pull request:
1. Test all modified endpoints
2. Ensure the application starts without errors
3. Verify no broken imports
4. Check that all features still work as expected

## Submitting Changes

1. Create a new branch for your feature/fix
2. Make your changes following the code style guidelines
3. Test your changes thoroughly
4. Commit with clear, descriptive messages
5. Push your branch and create a pull request

## Questions?

If you have questions, please open an issue on GitHub.
