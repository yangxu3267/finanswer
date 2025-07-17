# Contributing to Finanswer

Thank you for your interest in contributing to Finanswer! This document provides guidelines for contributing to the project.

## How to Contribute

### 1. Fork the Repository
- Fork the repository to your GitHub account
- Clone your fork locally

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Follow the coding standards
- Add tests for new features
- Update documentation as needed

### 4. Test Your Changes
- Run the backend server: `python backend/server.py`
- Test the Chrome extension
- Ensure all tests pass

### 5. Submit a Pull Request
- Push your changes to your fork
- Create a pull request with a clear description
- Reference any related issues

## Development Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python server.py
```

### Chrome Extension
- Load the extension from the `extension` folder in Chrome

## Code of Conduct
Please be respectful and constructive in all interactions.

## Code Standards

### Python
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Add comments for complex logic

### HTML/CSS
- Use semantic HTML
- Follow BEM methodology for CSS
- Ensure responsive design

## Testing

### Backend Tests
```bash
cd tests
python -m pytest test_*.py
```

### Extension Tests
- Test on different financial news websites
- Verify sentiment analysis accuracy
- Check UI responsiveness

## Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Browser and OS information
- Any error messages

## Feature Requests

For feature requests:
- Describe the feature clearly
- Explain the use case
- Consider implementation complexity
- Check if it aligns with project goals

## Questions?

Feel free to open an issue for questions or discussions about the project.

Thank you for contributing to Finanswer! 🚀 