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
3. **Test changes locally** - Use `apify run` before deploying
4. **Update schema if needed** - Add new fields to input schema
5. **Deploy** - Push changes with `apify push`

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

## Best Practices

### Code Quality

1. **Validate input** - Always check required fields and formats with clear error messages
2. **Handle errors** - Use try/catch with proper error logging and graceful degradation
3. **Structured logging** - Use Actor.log with extra fields for better debugging
4. **Type hints** - Add type annotations for better code clarity and IDE support
5. **Docstrings** - Document functions and modules for maintainability

### Performance & Scalability

6. **Batch processing** - Push data in batches (100-1000 items) for large datasets
7. **Use proxies** - Avoid IP blocking for web scraping
8. **Resource limits** - Set appropriate memory and timeout in actor.json
9. **Optimize Docker** - Use multi-stage builds and bytecode compilation
10. **Consider Standby mode** - For low-latency, high-frequency use cases

### Security & Configuration

11. **Environment variables** - Never hardcode secrets, use Actor.config and env vars
12. **Input validation** - Use JSON Schema patterns and required fields
13. **Run as non-root** - Use myuser in Dockerfile for security
14. **Minimize image size** - Use .dockerignore to exclude unnecessary files

### Development Workflow

15. **Testing** - Write tests with pytest, use coverage and snapshot testing
16. **Pre-commit hooks** - Use ruff and pre-commit for consistent code quality
17. **Lock dependencies** - Use uv.lock or similar for reproducible builds
18. **Test locally** - Always test with `apify run` before deploying
19. **Dataset schemas** - Define dataset_schema.json with views for better UI
20. **CLI support** - Add CLI entry points for local testing and development

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
