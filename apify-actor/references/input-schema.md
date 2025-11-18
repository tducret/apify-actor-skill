# Input Schema Reference

Input schemas define and validate actor inputs using JSON Schema format (`.actor/input_schema.json`).

## Structure

```json
{
    "title": "Actor Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": { /* fields */ },
    "required": ["fieldName"]
}
```

## Field Types

- **string**: `{"type": "string", "pattern": "^https?://", "example": "..."}`
- **integer**: `{"type": "integer", "minimum": 1, "maximum": 100, "default": 10, "unit": "pages"}`
- **boolean**: `{"type": "boolean", "default": false}`
- **array**: `{"type": "array", "items": {"type": "string"}}`
- **enum**: `{"type": "string", "enum": ["a", "b"], "editor": "select"}`
- **object**: `{"type": "object", "properties": {...}}`

## Special Editors

- **requestListSources**: URL list input
- **globs**: URL pattern matching
- **pseudoUrls**: URL pattern extraction
- **proxy**: Proxy configuration UI
- **json**: JSON editor with validation
- **textarea**: Multi-line text input

## Complete Example

```json
{
    "title": "E-commerce Scraper Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "array",
            "description": "List of product listing pages to scrape",
            "editor": "requestListSources",
            "placeholderKey": "startUrls",
            "placeholderValue": "https://example.com/products"
        },
        "maxPages": {
            "title": "Maximum pages",
            "type": "integer",
            "description": "Maximum number of pages to scrape",
            "default": 100,
            "minimum": 1,
            "maximum": 10000,
            "unit": "pages"
        },
        "proxyConfiguration": {
            "title": "Proxy configuration",
            "type": "object",
            "description": "Proxy settings for avoiding blocks",
            "editor": "proxy",
            "default": {
                "useApifyProxy": true
            }
        },
        "includeImages": {
            "title": "Include product images",
            "type": "boolean",
            "description": "Whether to download product images",
            "default": false
        },
        "outputFormat": {
            "title": "Output format",
            "type": "string",
            "description": "Format of the output data",
            "enum": ["json", "csv", "xlsx"],
            "enumTitles": ["JSON", "CSV", "Excel"],
            "default": "json",
            "editor": "select"
        },
        "filters": {
            "title": "Filters",
            "type": "object",
            "description": "Product filters",
            "editor": "json",
            "properties": {
                "minPrice": {
                    "type": "number",
                    "title": "Minimum price"
                },
                "maxPrice": {
                    "type": "number",
                    "title": "Maximum price"
                },
                "categories": {
                    "type": "array",
                    "title": "Categories",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    },
    "required": ["startUrls"]
}
```

## Validation

- **pattern**: `"pattern": "^https?://.+"` (regex)
- **length**: `"minLength": 10, "maxLength": 100`
- **range**: `"minimum": 0, "maximum": 300`
- **required**: `"required": ["fieldName"]` (at schema level)

## Best Practices

- Include descriptions and examples for all fields
- Set sensible defaults for easy usage
- Use appropriate editors (requestListSources, proxy, json, etc.)
- Validate with patterns, min/max, and required fields
- Add units for numbers (pages, seconds, MB)
