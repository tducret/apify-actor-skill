---
name: apify-actor
description: Build and deploy Apify actors for web scraping and automation. Use for serverless scraping, data extraction, browser automation, and API integrations with Python.
---

# Apify Actor Development

Build serverless Apify actors for web scraping, browser automation, and data extraction using Python.

> **Note**: For detailed official documentation beyond this skill, refer to https://docs.apify.com/llms.txt

## Prerequisites & Setup

Install the Apify CLI and authenticate (run `apify --help` for more details):

```bash
brew install apify-cli  # macOS

# Or (Windows (PowerShell)): irm https://apify.com/install-cli.ps1 | iex
# Or: npm install -g apify-cli
# Or: curl -fsSL https://apify.com/install-cli.sh | bash

apify login  # Authenticate with your account
```

If you need information not covered in this skill, use the WebFetch tool with https://docs.apify.com/llms.txt to access the complete official documentation.

## Quick Start Workflow

### Creating a New Actor

**Using Apify CLI (recommended for official templates):**

```bash
apify create my-actor
```

This provides access to official templates optimized for different use cases.

**Using skill templates (for simple actors):**

For basic actors, copy from `assets/python-template/` to get started quickly with a minimal structure.

### Development Process

1. **Initialize/Create** - Use `apify create` or copy skill template
2. **Develop** - Implement actor logic in `src/main.py`
3. **Configure Input** - Define input schema in `.actor/input_schema.json`
4. **Configure Output** - Define output schema in `.actor/output_schema.json`
5. **Write Documentation** - Create comprehensive `.actor/ACTOR.md` (public-facing docs)
6. **Test Locally** - Run with `apify run` to test functionality
7. **Deploy** - Push to platform with `apify push`

## Why Python

Python is excellent for Apify actors because:
- Rich ecosystem for data processing (pandas, numpy, scikit-learn)
- Popular scraping libraries (BeautifulSoup, Scrapy, lxml)
- Clean async/await syntax with asyncio
- Strong support for browser automation (Playwright, Selenium)
- Fast HTTP libraries (httpx, curl-cffi for impersonation)
- Full SDK support and access to all Apify features

## Dependency Management (MANDATORY)

**ALWAYS use `uv` for dependency management. NEVER use `pip` or create `requirements.txt` files.**

### Required tooling:

1. **uv** - Fast Python package manager
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Dependencies**:
   - Use `pyproject.toml` to declare dependencies (NOT requirements.txt)
   - Use `uv sync` to install dependencies (NOT `uv pip install` or `pip install`)
   - Lock file (`uv.lock`) is automatically generated and MUST be committed

### Commands:

```bash
# Add a dependency
uv add apify httpx beautifulsoup4

# Add a dev dependency
uv add --dev pytest ruff pre-commit

# Install all dependencies (creates .venv)
uv sync

# Install without dev dependencies (for Docker)
uv sync --frozen --no-dev

# Update dependencies
uv sync --upgrade
```

### In Docker:

The template already uses `uv sync --frozen --no-dev` in the Dockerfile. Never modify this to use pip.

## Core Concepts

### Input/Output Pattern

Every actor follows this pattern:

1. **Input**: JSON from key-value store (defined by input schema)
2. **Process**: Actor logic extracts/transforms data
3. **Output**: Results pushed to dataset or key-value store

### Storage Types

- **Dataset**: Structured data (arrays of objects) - use for scraping results
- **Key-Value Store**: Arbitrary data (files, objects) - use for screenshots, PDFs, state
- **Request Queue**: URLs to crawl - use for deep crawling workflows

### Project Structure

```
my-actor/
├── .actor/
│   ├── actor.json                    # Actor metadata
│   ├── input_schema.json             # Input schema
│   ├── output_schema.json            # Output schema
│   ├── ACTOR.md                      # PUBLIC marketplace documentation (CRITICAL)
│   └── datasets/
│       └── dataset_schema.json       # Dataset schema with views
├── src/ or package_name/             # Source code
│   ├── __init__.py
│   ├── __main__.py                   # Module execution entry
│   └── main.py                       # Main actor logic
├── tests/                            # Test files
│   └── test_*.py
├── .dockerignore                     # Docker build exclusions
├── .pre-commit-config.yaml           # Pre-commit hooks
├── Dockerfile                        # Container config
├── pyproject.toml                    # Python project config
├── uv.lock                          # Dependency lock file
└── README.md                         # Development docs
```

## Common Patterns

See `references/python-sdk.md` for complete examples:
- Simple HTTP scraping with BeautifulSoup
- Browser automation with Playwright/Selenium
- Deep crawling with Request Queue
- Proxy management and error handling

### Standby Mode (Real-time API)

Deploy actors as persistent HTTP servers for instant responses without cold starts. See `references/standby-mode.md` for complete implementation patterns.

## Input Schema Design

Input schemas use JSON Schema format to define actor inputs. See `references/input-schema.md` for:

- Field types (string, number, boolean, array, object)
- Special editors (URLs, proxies, JSON)
- Validation patterns
- Complete examples

**Key principles:**
- Always include descriptions
- Provide examples
- Set sensible defaults
- Use appropriate editors

## Output Schema Design

Output schemas define where actors store outputs and provide templates for accessing data. See `references/output-schema.md` for:

- Schema structure and template variables
- Dataset and key-value store outputs
- Multiple output types
- Integration with code
- Complete examples

**Key principles:**
- Define all outputs explicitly
- Use descriptive titles with emojis
- Include helpful descriptions
- Match templates to actual storage locations

## ACTOR.md Documentation (CRITICAL)

The `.actor/ACTOR.md` file is **the public-facing documentation** that users see in the Apify marketplace. This is your actor's main sales page and user guide.

**Required sections:**
1. **Title & Description** - Clear, compelling one-liner
2. **What it does** - Bullet points of key capabilities
3. **Input** - Example JSON with field explanations
4. **Output** - Example JSON showing expected results
5. **Use Cases** - Who benefits and why (with emojis)
6. **Standby Mode** (if applicable) - API usage examples
7. **Tips & Best Practices** - Performance and configuration guidance

See `assets/python-template/.actor/ACTOR.md` for a complete template.

**Key principles:**
- Write for non-technical users - assume no coding knowledge
- Use emojis to make sections scannable (🎯 🔍 ⚡ 🚀)
- Provide copy-paste ready code examples
- Show actual input/output samples, not schemas
- Highlight benefits and use cases clearly

## Essential Commands

```bash
apify login              # Authenticate
apify create my-actor    # Create new actor
apify run               # Test locally
apify push              # Deploy to platform
apify call my-actor     # Run on platform
```

For more commands and options, run `apify --help` or `apify <command> --help`.

## Modifying Existing Actors

When modifying an existing actor:

1. **Understand current logic** - Read `src/main.py`
2. **Check input schema** - Review `.actor/input_schema.json` for expected inputs
3. **Add dependencies with uv** - Use `uv add package-name` (NEVER pip install)
4. **Make code changes** - Implement the requested features
5. **Format code** - Run `uv run ruff format .` (MANDATORY)
6. **Lint code** - Run `uv run ruff check --fix .` (MANDATORY)
7. **Test changes locally** - Use `apify run` before deploying
8. **Update schema if needed** - Add new fields to input schema
9. **Deploy** - Push changes with `apify push`

## Creating New Actors - Claude Workflow

When creating a new actor, Claude should follow this workflow:

1. **Copy template** - Use files from `assets/python-template/`
2. **Add dependencies** - Use `uv add package-name` for each required dependency
3. **Implement logic** - Write the actor code in `src/main.py`
4. **Format code** - Run `uv run ruff format .` (MANDATORY before testing)
5. **Lint code** - Run `uv run ruff check --fix .` (MANDATORY before testing)
6. **Configure schemas** - Update input/output schemas
7. **Write documentation** - Create comprehensive `.actor/ACTOR.md`
8. **Test locally** - Run `apify run` to verify functionality
9. **Setup pre-commit** - Run `uv run pre-commit install` for automatic quality checks

**CRITICAL REMINDERS:**
- NEVER create `requirements.txt`
- NEVER use `pip install` or `uv pip install`
- ALWAYS use `uv add` to add dependencies
- ALWAYS use `uv sync` to install dependencies
- ALWAYS format with `uv run ruff format .` before committing/testing
- ALWAYS lint with `uv run ruff check --fix .` before deploying

## Debugging Actors

### Local Debugging

1. Use `apify run` to test locally
2. Check `./storage/` directory for output
3. Add logging statements (see SDK references)
4. Use IDE debugger with breakpoints

### Platform Debugging

1. View logs in Apify Console
2. Check run details for errors
3. Download datasets/stores to inspect output
4. Test with different inputs

### Common Issues

- **Timeouts**: Increase timeout or optimize code
- **Memory errors**: Process in batches, increase memory
- **Network errors**: Implement retries, use proxies
- **Build failures**: Check Dockerfile and dependencies

## Code Quality & Formatting (MANDATORY)

**ALWAYS format and check code with ruff before committing or deploying.**

### Required quality tooling:

1. **ruff** - Fast Python linter and formatter (replaces black, flake8, isort)
   ```bash
   # Install with uv
   uv add --dev ruff

   # Format code
   uv run ruff format .

   # Check and fix linting issues
   uv run ruff check --fix .

   # Check without auto-fix
   uv run ruff check .
   ```

2. **pre-commit** - Automatically run ruff on every commit
   ```bash
   # Install with uv
   uv add --dev pre-commit

   # Setup hooks
   uv run pre-commit install

   # Run manually
   uv run pre-commit run --all-files
   ```

The template includes a `.pre-commit-config.yaml` that runs:
- `ruff` - Linting with auto-fix
- `ruff-format` - Code formatting
- Standard hooks (trailing whitespace, YAML validation, etc.)

### Workflow:

```bash
# Before committing
uv run ruff format .
uv run ruff check --fix .

# Or let pre-commit handle it automatically
git commit -m "your message"  # pre-commit runs automatically
```

## Best Practices

### Code Quality

1. **Validate input** - Always check required fields and formats with clear error messages
2. **Handle errors** - Use try/catch with proper error logging and graceful degradation
3. **Structured logging** - Use Actor.log with extra fields for better debugging
4. **Type hints** - Add type annotations for better code clarity and IDE support
5. **Docstrings** - Document functions and modules for maintainability
6. **Format with ruff** - ALWAYS run `uv run ruff format .` before committing
7. **Lint with ruff** - ALWAYS run `uv run ruff check --fix .` before deploying

### Performance & Scalability

8. **Batch processing** - Push data in batches (100-1000 items) for large datasets
9. **Use proxies** - Avoid IP blocking for web scraping
10. **Resource limits** - Set appropriate memory and timeout in actor.json
11. **Optimize Docker** - Use multi-stage builds and bytecode compilation
12. **Consider Standby mode** - For low-latency, high-frequency use cases

### Security & Configuration

13. **Environment variables** - Never hardcode secrets, use Actor.config and env vars
14. **Input validation** - Use JSON Schema patterns and required fields
15. **Run as non-root** - Use myuser in Dockerfile for security
16. **Minimize image size** - Use .dockerignore to exclude unnecessary files

### Development Workflow

17. **Testing** - Write tests with pytest, use coverage and snapshot testing
18. **Pre-commit hooks** - Use ruff and pre-commit for consistent code quality (MANDATORY)
19. **Use uv exclusively** - NEVER use pip or requirements.txt, only `uv sync` (MANDATORY)
20. **Lock dependencies** - Commit uv.lock for reproducible builds (MANDATORY)
21. **Test locally** - Always test with `apify run` before deploying
22. **Dataset schemas** - Define dataset_schema.json with views for better UI
23. **CLI support** - Add CLI entry points for local testing and development

## References

Detailed documentation in `references/`:

- `python-sdk.md` - SDK patterns and complete code examples
- `standby-mode.md` - Real-time API implementation
- `input-schema.md` - Input validation and UI configuration
- `output-schema.md` - Output configuration and templates

## Template

Minimal boilerplate template available in `assets/`:

- `python-template/` - Basic Python actor structure

Copy this for simple actors or use `apify create` for official templates with more features.
