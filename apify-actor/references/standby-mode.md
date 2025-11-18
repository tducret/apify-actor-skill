# Standby Mode Reference

Standby mode allows actors to run as persistent HTTP servers, providing instant responses without cold start delays.

## When to Use Standby Mode

**Perfect for:**
- Real-time APIs requiring <100ms response times
- Webhook endpoints that need immediate processing
- High-frequency requests (multiple per second)
- Integration with real-time services (Slack bots, chat applications)
- Low-latency scraping APIs

**Not recommended for:**
- Long-running batch jobs
- Infrequent scheduled tasks
- Memory-intensive processing
- Tasks that take >30 seconds per request

## Prerequisites

Standby mode requires the `aiohttp` library for the web server. Add it to your project:

```bash
uv add aiohttp
```

After adding dependencies, verify the Docker build works:

```bash
docker build .
```

## Basic Implementation

### Dual-Mode Actor

```python
from apify import Actor
from aiohttp import web
from crawlee.events import Event
import asyncio

async def handle_standby_request(request: web.Request) -> web.Response:
    """Handle HTTP requests in standby mode."""
    # Handle readiness probe (required)
    if "x-apify-container-server-readiness-probe" in request.headers:
        return web.Response(text="Ready!", status=200)

    # Get input from query params or JSON body
    url = None
    if request.method == "GET":
        url = request.query.get("url")
    elif request.method == "POST":
        try:
            data = await request.json()
            url = data.get("url")
        except Exception:
            return web.json_response(
                {"error": "Invalid JSON body"},
                status=400
            )

    if not url:
        return web.json_response(
            {
                "error": "Missing 'url' parameter. "
                        "Provide as query param (GET) or in JSON body (POST)"
            },
            status=400
        )

    # Process the request
    try:
        Actor.log.info(f"Processing request for URL: {url}")
        result = await process_url(url)
        Actor.log.info(f"Request completed for {url}")
        return web.json_response(result, status=200)
    except Exception as e:
        Actor.log.exception(f"Error processing URL {url}: {e}")
        return web.json_response(
            {"error": str(e)},
            status=500
        )


async def run_standby_mode() -> None:
    """Run the actor in standby mode as a web server."""
    Actor.log.info("Starting actor in standby mode")

    # Set up web application
    app = web.Application()
    app.router.add_get("/", handle_standby_request)
    app.router.add_post("/", handle_standby_request)

    runner = web.AppRunner(app)
    await runner.setup()

    # Start server on Apify's configured port
    port = Actor.configuration.web_server_port
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    Actor.log.info(
        f"Web server started on port {port}. "
        f"Standby URL: {Actor.configuration.standby_url or 'Not available'}"
    )

    # Set up graceful shutdown
    shutdown_event = asyncio.Event()

    async def on_aborting(_data):
        """Handle actor abort event."""
        Actor.log.info("Actor is aborting, initiating graceful shutdown...")
        shutdown_event.set()

    Actor.on(Event.ABORTING, on_aborting)

    # Keep server running until shutdown
    try:
        await shutdown_event.wait()
    finally:
        Actor.log.info("Shutting down web server...")
        await site.stop()
        await runner.cleanup()
        Actor.log.info("Web server shut down successfully")


async def run_classic_mode() -> None:
    """Run the actor in classic mode (single task execution)."""
    Actor.log.info("Starting actor in classic mode")

    actor_input = await Actor.get_input()
    assert "url" in actor_input, "Input must contain a 'url' field."

    url = actor_input["url"]
    Actor.log.info(f"Processing {url}")

    result = await process_url(url)
    await Actor.push_data(result)


async def main() -> None:
    """Main entry point that auto-detects mode."""
    async with Actor:
        # Detect if running in standby mode
        if Actor.configuration.meta_origin == "STANDBY":
            await run_standby_mode()
        else:
            await run_classic_mode()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

## Making Requests to Standby Actors

### GET Request (Query Parameters)

```bash
# Basic request with token in query
curl "https://YOUR_USERNAME--ACTOR_NAME.apify.actor?token=YOUR_TOKEN&url=https://example.com"

# With URL encoding for complex parameters
curl "https://YOUR_USERNAME--ACTOR_NAME.apify.actor?token=YOUR_TOKEN&url=https%3A%2F%2Fexample.com%2Fpath"
```

### POST Request (JSON Body)

```bash
# Using Authorization header (recommended)
curl -X POST https://YOUR_USERNAME--ACTOR_NAME.apify.actor \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"url": "https://example.com"}'

# Using token in query string
curl -X POST "https://YOUR_USERNAME--ACTOR_NAME.apify.actor?token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "maxItems": 100}'
```

### From Python

```python
import httpx
import os

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
STANDBY_URL = "https://YOUR_USERNAME--ACTOR_NAME.apify.actor"

async def call_standby_actor(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            STANDBY_URL,
            headers={"Authorization": f"Bearer {APIFY_TOKEN}"},
            json={"url": url}
        )
        return response.json()

# Usage
result = await call_standby_actor("https://example.com")
```

### From JavaScript

```javascript
const APIFY_TOKEN = process.env.APIFY_TOKEN;
const STANDBY_URL = 'https://YOUR_USERNAME--ACTOR_NAME.apify.actor';

async function callStandbyActor(url) {
    const response = await fetch(STANDBY_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${APIFY_TOKEN}`
        },
        body: JSON.stringify({ url })
    });
    return response.json();
}

// Usage
const result = await callStandbyActor('https://example.com');
```

## Authentication

### Getting Your Apify Token

1. Log in to [Apify Console](https://console.apify.com/)
2. Go to Settings > Integrations
3. Copy your API token
4. Keep it secure - never commit to version control

### Token Usage

**Query parameter:**
```
https://YOUR_USERNAME--ACTOR_NAME.apify.actor?token=YOUR_TOKEN&param=value
```

**Authorization header (recommended):**
```
Authorization: Bearer YOUR_TOKEN
```

The header method is more secure as tokens don't appear in URLs/logs.

## Best Practices

### 1. Handle Readiness Probes

Always respond to readiness probes:

```python
if "x-apify-container-server-readiness-probe" in request.headers:
    return web.Response(text="Ready!", status=200)
```

### 2. Implement Graceful Shutdown

Listen for ABORTING events and clean up resources:

```python
async def on_aborting(_data):
    Actor.log.info("Shutting down gracefully...")
    shutdown_event.set()

Actor.on(Event.ABORTING, on_aborting)
```

### 3. Use JSON Response Helper

For consistent JSON formatting:

```python
def json_dumps(obj) -> str:
    """Serialize to indented JSON with Unicode support."""
    return json.dumps(obj, indent=2, ensure_ascii=False)

# Use with aiohttp
return web.json_response(result, status=200, dumps=json_dumps)
```

### 4. Support Both GET and POST

GET is convenient for simple requests, POST for complex payloads:

```python
# GET: good for simple parameters
?url=https://example.com&maxItems=10

# POST: better for complex data, arrays, nested objects
{"url": "https://example.com", "filters": {"category": "tech"}}
```

### 5. Validate Input Thoroughly

```python
if not url:
    return web.json_response(
        {"error": "Missing required parameter: url"},
        status=400
    )

if not url.startswith(("http://", "https://")):
    return web.json_response(
        {"error": "URL must start with http:// or https://"},
        status=400
    )
```

### 6. Return Consistent Error Formats

```python
# Success
{"status": "success", "data": {...}}

# Error
{"status": "error", "error": "Error message", "code": "ERROR_CODE"}
```

### 7. Log All Requests

```python
Actor.log.info(
    f"Request received",
    extra={"url": url, "method": request.method}
)
```

### 8. Set Appropriate Timeouts

Don't let requests hang forever:

```python
async with asyncio.timeout(30):
    result = await process_url(url)
```

## Configuration

### actor.json

```json
{
    "actorSpecification": 1,
    "name": "my-actor",
    "title": "My Actor",
    "version": "1.0",
    "standbyMode": {
        "minReplicas": 1,
        "maxReplicas": 10
    },
    "minMemoryMbytes": 256,
    "maxMemoryMbytes": 512
}
```

### Standby Configuration

- **minReplicas**: Minimum instances always running (0-10)
- **maxReplicas**: Maximum instances during high load (1-100)
- **Memory**: Affects instance capacity and cost

## Monitoring

### Viewing Logs

Logs are available in real-time in the Apify Console:
1. Go to your actor
2. Click on "API" tab
3. View request logs and metrics

### Metrics to Monitor

- Request latency (p50, p95, p99)
- Error rate
- Active replicas
- CPU and memory usage
- Request throughput

## Cost Optimization

1. **Set minReplicas=1** for development, increase for production
2. **Use smallest memory** that meets performance needs
3. **Implement caching** for frequently requested data
4. **Monitor idle time** and adjust minReplicas accordingly
5. **Consider rate limiting** to prevent abuse

## Limitations

- Maximum request timeout: typically 30-60 seconds
- No direct file uploads (use signed URLs)
- Stateless - no persistent storage between requests
- Cold start when scaling from 0 replicas

## Example Use Cases

### 1. Web Scraping API

```python
async def handle_standby_request(request: web.Request) -> web.Response:
    url = request.query.get("url")
    selector = request.query.get("selector", "body")

    html = await fetch_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.select(selector)

    return web.json_response({
        "url": url,
        "content": [el.text for el in content]
    })
```

### 2. XPath Generator

```python
async def handle_standby_request(request: web.Request) -> web.Response:
    url = request.query.get("url")

    html = await fetch_url(url)
    xpaths = generate_xpaths(html)

    return web.json_response({
        "url": url,
        "xpaths": xpaths
    })
```

### 3. Webhook Processor

```python
async def handle_standby_request(request: web.Request) -> web.Response:
    data = await request.json()

    # Process webhook immediately
    result = await process_webhook(data)

    # Optionally save to dataset for later analysis
    from datetime import datetime, timezone
    await Actor.push_data({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
        "result": result
    })

    return web.json_response({"status": "processed", "result": result})
```

## Resources

- [Standby Mode Documentation](https://docs.apify.com/platform/actors/running/standby)
- [Actor API Reference](https://docs.apify.com/api/v2#/reference/actors)
- [aiohttp Documentation](https://docs.aiohttp.org/)
