# Actor Name

Brief one-line description of what your actor does.

**What it does:**
- **Action 1** - Description of first main capability
- **Action 2** - Description of second main capability
- **Action 3** - Description of third main capability

## Input

```json
{
  "url": "https://example.com",
  "maxPages": 10
}
```

**Required fields:**
- `url` - The target URL to process

**Optional fields:**
- `maxPages` - Maximum number of pages (default: 10)

## Output

```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

## Example Use Cases

**🎯 Use Case 1**
Brief description of who would use this and why.

**🔍 Use Case 2**
Brief description of another common use case.

**⚡ Use Case 3**
Brief description of a third use case.

## Standby Mode (Real-time API)

For faster results without cold starts, use this actor as a real-time API:

```bash
TOKEN="REPLACE_WITH_YOUR_APIFY_TOKEN"

curl "https://YOUR_USERNAME--actor-name.apify.actor?token=${TOKEN}&url=https://example.com"

# Or as a POST request with JSON body
curl -X POST https://YOUR_USERNAME--actor-name.apify.actor \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"url": "https://example.com"}'
```

Check [the documentation](https://docs.apify.com/platform/actors/running/standby#how-do-i-authenticate-my-requests) to learn how to obtain your Apify token.

**Benefits:**
- ⚡ **Instant response** - No cold start delays
- 📈 **Auto-scaling** - Handles varying request loads
- 🔄 **Persistent** - Always ready to serve requests

## Tips & Best Practices

- **Performance tip** - Suggestions for optimal usage
- **Configuration tip** - How to configure for specific needs
- **Troubleshooting** - Common issues and solutions
