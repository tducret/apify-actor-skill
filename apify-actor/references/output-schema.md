# Output Schema Reference

Output schemas define where actors store their outputs and provide templates for accessing that data. They enable the Apify Console to display run results and the API to include output definitions.

## Basic Schema Structure

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "Actor Output Schema",
    "description": "Defines the outputs produced by this actor",
    "properties": {
        "dataset": {
            "title": "Scraped data",
            "description": "Collection of scraped items",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        }
    }
}
```

## File Location

Output schemas are stored in the `.actor` directory:

**Option 1: Separate file (recommended)**
```
my-actor/
├── .actor/
│   ├── actor.json
│   ├── input_schema.json
│   └── output_schema.json    # Output schema file
```

In `actor.json`, reference it:
```json
{
    "name": "my-actor",
    "version": "1.0",
    "outputSchema": "./output_schema.json"
}
```

**Option 2: Inline in actor.json**
```json
{
    "name": "my-actor",
    "version": "1.0",
    "outputSchema": {
        "actorOutputSchemaVersion": 1,
        "title": "My Actor Output",
        "properties": {...}
    }
}
```

## Schema Properties

### Required Fields

- `actorOutputSchemaVersion` (integer): Schema version, currently only `1` is supported
- `title` (string): Human-readable name for the schema
- `properties` (object): Defines each output with its template

### Optional Fields

- `description` (string): Additional context about the outputs

## Property Object

Each property in `properties` defines an output:

```json
{
    "propertyName": {
        "title": "Display Name",
        "description": "Helpful description for users and LLMs",
        "template": "{{templateVariable}}/path"
    }
}
```

**Fields:**
- `title` (required): Display name shown in Console and API
- `description` (optional): Helpful for documentation and LLM integrations
- `template` (required): URL pattern using template variables

## Template Variables

Use these variables to construct output URLs:

### Dataset Variables

```
{{links.apiDefaultDatasetUrl}}
```

Full dataset API endpoint. Example usage:
```json
{
    "items": {
        "title": "Scraped items",
        "template": "{{links.apiDefaultDatasetUrl}}/items"
    }
}
```

### Key-Value Store Variables

```
{{links.apiDefaultKeyValueStoreUrl}}
```

Key-value store API endpoint. Example usage:
```json
{
    "screenshot": {
        "title": "Screenshot",
        "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/screenshot.png"
    }
}
```

### Run Variables

```
{{run.containerUrl}}
```

Web server URL running inside the actor. Example:
```json
{
    "dashboard": {
        "title": "Live Dashboard",
        "template": "{{run.containerUrl}}/dashboard"
    }
}
```

### Other Variables

- `{{links.apiDefaultRequestQueueUrl}}` - Request queue API endpoint
- `{{run.defaultDatasetId}}` - Dataset ID
- `{{run.defaultKeyValueStoreId}}` - Key-value store ID

## Common Patterns

### Dataset Outputs

For scraped data stored in dataset:

```json
{
    "properties": {
        "dataset": {
            "title": "Scraped products",
            "description": "Product data extracted from the website",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        }
    }
}
```

### Dataset with Views

For specific dataset views:

```json
{
    "properties": {
        "products": {
            "title": "Products",
            "template": "{{links.apiDefaultDatasetUrl}}/items?view=products"
        },
        "reviews": {
            "title": "Reviews",
            "template": "{{links.apiDefaultDatasetUrl}}/items?view=reviews"
        }
    }
}
```

### Key-Value Store Files

For files stored in key-value store:

```json
{
    "properties": {
        "screenshot": {
            "title": "Screenshot",
            "description": "Screenshot of the scraped page",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/screenshot.png"
        },
        "pdf": {
            "title": "PDF Report",
            "description": "Generated PDF report",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/report.pdf"
        },
        "summary": {
            "title": "Summary JSON",
            "description": "Summary statistics",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/summary.json"
        }
    }
}
```

### Multiple Output Types

Combining different output types:

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "E-commerce Scraper Output",
    "description": "Product data, images, and analytics",
    "properties": {
        "products": {
            "title": "Product data",
            "description": "Scraped product information",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        },
        "images": {
            "title": "Product images",
            "description": "Downloaded product images",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys?collection=images"
        },
        "analytics": {
            "title": "Analytics report",
            "description": "Summary statistics and insights",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/analytics.json"
        }
    }
}
```

## No Output Schema

For actors that don't produce outputs (utility actors):

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "No Output",
    "description": "This actor performs an action but does not produce output data",
    "properties": {}
}
```

This prevents confusion about failed runs vs. actors with no output.

## Complete Example

E-commerce scraper with multiple outputs:

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "E-commerce Scraper Output",
    "description": "Product listings, images, and run statistics",
    "properties": {
        "dataset": {
            "title": "📦 Product listings",
            "description": "Complete product data including prices, descriptions, and ratings",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        },
        "images": {
            "title": "🖼️ Product images",
            "description": "Downloaded product images organized by SKU",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys?collection=images"
        },
        "screenshot": {
            "title": "📸 Page screenshot",
            "description": "Screenshot of the last scraped page",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/screenshot.png"
        },
        "stats": {
            "title": "📊 Run statistics",
            "description": "Summary of items scraped, errors, and performance metrics",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/stats.json"
        },
        "errors": {
            "title": "⚠️ Error log",
            "description": "List of URLs that failed to scrape with error details",
            "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys/errors.json"
        }
    }
}
```

## Best Practices

1. **Define outputs explicitly** - Always create an output schema, even if empty
2. **Use descriptive titles** - Help users understand what each output contains
3. **Add emojis to titles** - Improves visual clarity in Console UI (📦, 🖼️, 📊, etc.)
4. **Include descriptions** - Especially helpful for LLM integrations
5. **Organize with views/collections** - Use query parameters for complex outputs
6. **Match your code** - Ensure templates match where your code actually saves data
7. **Document file formats** - Specify extensions in titles (JSON, PNG, CSV, etc.)

## Integration with Code

Your Python code should match the output schema:

```python
from apify import Actor

async def main():
    async with Actor:
        # Push to dataset (matches "dataset" property)
        await Actor.push_data({
            'title': 'Product name',
            'price': 29.99
        })

        # Save screenshot (matches "screenshot" property)
        await Actor.set_value('screenshot.png', screenshot_bytes,
                             content_type='image/png')

        # Save summary (matches "summary" property)
        await Actor.set_value('summary.json', {
            'items_scraped': 100,
            'duration': 45.2
        })
```

## Viewing Outputs

After defining an output schema:

1. **Apify Console**: Run details page shows outputs with titles and links
2. **API**: `GET /v2/acts/{actorId}/runs/{runId}` includes output definitions
3. **Integrations**: Tools and LLMs can discover outputs automatically

## Related Documentation

- **Input Schemas**: See `input-schema.md` for defining actor inputs
- **Python SDK**: See `python-sdk.md` for saving data to dataset and key-value store
- **Storage**: Dataset for structured data, Key-Value Store for files and objects
