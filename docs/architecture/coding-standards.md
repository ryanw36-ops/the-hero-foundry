# Coding Standards - The Hero Foundry

## Overview
This document defines the coding standards and best practices for The Hero Foundry project. All developers must follow these standards to ensure code quality, consistency, and maintainability.

## Python Coding Standards

### Code Style
- **PEP 8 Compliance:** Follow Python PEP 8 style guide
- **Line Length:** Maximum 88 characters (Black formatter default)
- **Indentation:** 4 spaces (no tabs)
- **String Quotes:** Use double quotes for strings, single quotes for characters

### Naming Conventions
- **Classes:** PascalCase (e.g., `HeroManager`, `StoryBuilder`)
- **Functions/Methods:** snake_case (e.g., `create_hero`, `get_story_by_id`)
- **Variables:** snake_case (e.g., `hero_name`, `story_title`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_HERO_LEVEL`, `DEFAULT_ATTRIBUTES`)
- **Private Methods:** Prefix with underscore (e.g., `_validate_attributes`)

### File Organization
```
src/
├── hero_foundry/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── hero.py
│   │   ├── story.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── hero_service.py
│   │   └── story_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── middleware/
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
```

### Import Organization
```python
# Standard library imports
import os
import sys
from typing import Dict, List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

# Local imports
from hero_foundry.models.hero import Hero
from hero_foundry.services.hero_service import HeroService
```

## Type Hints
- **Always use type hints** for function parameters and return values
- **Use Optional[]** for nullable values
- **Use Union[]** for multiple possible types
- **Use generics** for collections

```python
def create_hero(
    name: str,
    attributes: Dict[str, int],
    owner_id: str,
    template_id: Optional[str] = None
) -> Hero:
    """Create a new hero with the given attributes."""
    pass

def get_heroes_by_owner(owner_id: str) -> List[Hero]:
    """Retrieve all heroes owned by a specific user."""
    pass
```

## Documentation Standards

### Docstrings
- **Use Google-style docstrings** for all public functions and classes
- **Include type information** in docstring parameters
- **Provide examples** for complex functions

```python
def calculate_hero_power_level(hero: Hero) -> int:
    """Calculate the power level of a hero based on their attributes.
    
    Args:
        hero: The hero object containing attributes and skills
        
    Returns:
        An integer representing the hero's power level
        
    Raises:
        ValueError: If hero has invalid attributes
        
    Example:
        >>> hero = Hero(name="Aragorn", attributes={"strength": 18, "agility": 16})
        >>> calculate_hero_power_level(hero)
        34
    """
    pass
```

### Inline Comments
- **Explain complex logic** with clear, concise comments
- **Avoid obvious comments** that just restate the code
- **Use TODO comments** for future improvements

```python
# Calculate weighted average of attributes (strength counts double)
power_level = (hero.attributes.get("strength", 0) * 2 + 
               hero.attributes.get("agility", 0) + 
               hero.attributes.get("intelligence", 0)) // 4

# TODO: Add support for magical items that modify power level
```

## Error Handling

### Exception Handling
- **Use specific exceptions** rather than generic ones
- **Log errors** with appropriate context
- **Return meaningful error messages** to users
- **Use custom exception classes** for domain-specific errors

```python
class HeroValidationError(Exception):
    """Raised when hero data validation fails."""
    pass

class HeroNotFoundError(Exception):
    """Raised when a hero cannot be found."""
    pass

def create_hero(name: str, attributes: Dict[str, int]) -> Hero:
    try:
        if not name or len(name.strip()) == 0:
            raise HeroValidationError("Hero name cannot be empty")
        
        if not attributes:
            raise HeroValidationError("Hero must have at least one attribute")
            
        # Create hero logic here
        return Hero(name=name, attributes=attributes)
        
    except Exception as e:
        logger.error(f"Failed to create hero '{name}': {str(e)}")
        raise
```

### Logging
- **Use structured logging** with consistent field names
- **Include context** in log messages
- **Use appropriate log levels** (DEBUG, INFO, WARNING, ERROR, CRITICAL)

```python
import logging

logger = logging.getLogger(__name__)

def create_hero(name: str, attributes: Dict[str, int]) -> Hero:
    logger.info("Creating new hero", extra={
        "hero_name": name,
        "attribute_count": len(attributes),
        "user_id": get_current_user_id()
    })
    
    try:
        hero = Hero(name=name, attributes=attributes)
        logger.info("Hero created successfully", extra={
            "hero_id": str(hero.id),
            "hero_name": hero.name
        })
        return hero
    except Exception as e:
        logger.error("Failed to create hero", extra={
            "hero_name": name,
            "error": str(e),
            "user_id": get_current_user_id()
        })
        raise
```

## Testing Standards

### Test Organization
- **Test files** should mirror the source code structure
- **Test classes** should test a single class or module
- **Test methods** should test a single behavior
- **Use descriptive test names** that explain what is being tested

```python
# tests/test_hero_service.py
import pytest
from hero_foundry.services.hero_service import HeroService
from hero_foundry.models.hero import Hero

class TestHeroService:
    """Test cases for HeroService class."""
    
    def test_create_hero_with_valid_data(self):
        """Test hero creation with valid input data."""
        service = HeroService()
        hero_data = {"name": "Test Hero", "attributes": {"strength": 15}}
        
        hero = service.create_hero(**hero_data)
        
        assert hero.name == "Test Hero"
        assert hero.attributes["strength"] == 15
        
    def test_create_hero_with_empty_name_raises_error(self):
        """Test that creating hero with empty name raises validation error."""
        service = HeroService()
        
        with pytest.raises(HeroValidationError, match="Hero name cannot be empty"):
            service.create_hero(name="", attributes={"strength": 15})
```

### Test Coverage
- **Aim for 90%+ code coverage** for all new code
- **Test both success and failure paths**
- **Test edge cases** and boundary conditions
- **Use mocking** for external dependencies

## Performance Standards

### Database Operations
- **Use database indexes** for frequently queried fields
- **Implement pagination** for large result sets
- **Use bulk operations** when possible
- **Avoid N+1 query problems**

### Caching
- **Cache frequently accessed data** in Redis
- **Use appropriate cache expiration** times
- **Implement cache invalidation** strategies
- **Monitor cache hit rates**

### Async Operations
- **Use async/await** for I/O operations
- **Implement background tasks** for long-running operations
- **Use connection pooling** for database connections
- **Handle timeouts** appropriately

## Security Standards

### Input Validation
- **Validate all user inputs** before processing
- **Sanitize data** to prevent injection attacks
- **Use parameterized queries** for database operations
- **Implement rate limiting** for API endpoints

### Authentication & Authorization
- **Use secure authentication** methods (JWT, OAuth)
- **Implement role-based access control**
- **Validate user permissions** for all operations
- **Log security events** for audit purposes

### Data Protection
- **Encrypt sensitive data** at rest and in transit
- **Use secure communication** protocols (HTTPS, TLS)
- **Implement proper session management**
- **Follow data privacy regulations** (GDPR, CCPA)

## Code Review Checklist

### Before Submitting Code
- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have proper type hints
- [ ] Docstrings are complete and accurate
- [ ] Error handling is implemented
- [ ] Logging is appropriate
- [ ] Tests are written and passing
- [ ] Code coverage meets requirements
- [ ] Security considerations are addressed

### During Code Review
- [ ] Code is readable and maintainable
- [ ] Logic is correct and efficient
- [ ] Error handling is comprehensive
- [ ] Tests cover all scenarios
- [ ] Documentation is clear and complete
- [ ] Performance implications are considered
- [ ] Security vulnerabilities are addressed

## Tools and Automation

### Code Formatting
- **Black:** Automatic code formatting
- **isort:** Import statement sorting
- **flake8:** Style and error checking

### Linting and Analysis
- **pylint:** Code quality analysis
- **mypy:** Static type checking
- **bandit:** Security vulnerability scanning

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Continuous Integration

### Automated Checks
- **Code formatting** validation
- **Linting** and style checking
- **Type checking** with mypy
- **Security scanning** with bandit
- **Test execution** and coverage reporting
- **Documentation** generation

### Quality Gates
- **All tests must pass**
- **Code coverage must be ≥90%**
- **No critical security vulnerabilities**
- **All linting errors must be resolved**
- **Documentation must be up to date**

---

*These coding standards ensure consistent, high-quality code across The Hero Foundry project. All developers are expected to follow these guidelines.*




