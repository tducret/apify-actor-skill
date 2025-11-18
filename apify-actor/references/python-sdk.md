# Python SDK Reference

## Basic Actor Structure

See `assets/python-template/src/main.py` for the complete boilerplate structure. Every actor follows this pattern:

1. Get input: `actor_input = await Actor.get_input() or {}`
2. Process data with your logic
3. Push results: `await Actor.push_data(results)`

## Input Handling

```python
# Get input with default values
actor_input = await Actor.get_input() or {}
start_url = actor_input.get('startUrl', 'https://example.com')
max_pages = actor_input.get('maxPages', 10)

# Validate required inputs
if not actor_input.get('apiKey'):
    raise ValueError('apiKey is required in input')
```

## Storage APIs

### Dataset (structured data)

```python
# Push single item
await Actor.push_data({'name': 'John', 'age': 30})

# Push multiple items
await Actor.push_data([
    {'name': 'John', 'age': 30},
    {'name': 'Jane', 'age': 25}
])

# Open named dataset
dataset = await Actor.open_dataset(name='my-dataset')
await dataset.push_data({'item': 'data'})
```

### Key-Value Store (arbitrary data)

```python
# Get/set values in default store
await Actor.set_value('KEY', {'any': 'data'})
value = await Actor.get_value('KEY')

# Open named store
store = await Actor.open_key_value_store(name='my-store')
await store.set_value('KEY', 'value')

# Store files (images, PDFs, etc.)
with open('screenshot.png', 'rb') as f:
    await Actor.set_value('screenshot', f.read(), content_type='image/png')
```

### Request Queue (crawling)

```python
# Open default queue
queue = await Actor.open_request_queue()

# Add URLs to crawl
await queue.add_request({'url': 'https://example.com'})
await queue.add_request({
    'url': 'https://example.com/page',
    'userData': {'label': 'DETAIL'}
})

# Process queue
while request := await queue.fetch_next_request():
    # Process request
    # ...
    await queue.mark_request_as_handled(request)
```

## Web Scraping

### Using HTTP Requests (httpx or curl-cffi)

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(url)
    await Actor.push_data({'html': response.text})
```

### Using BeautifulSoup

```python
from bs4 import BeautifulSoup
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data
    results = []
    for item in soup.select('.product'):
        results.append({
            'title': item.select_one('.title').text,
            'price': item.select_one('.price').text
        })

    await Actor.push_data(results)
```

### Using Playwright

```python
from playwright.async_api import async_playwright

async with async_playwright() as playwright:
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()

    await page.goto(url)
    await page.wait_for_selector('.content')

    # Extract data
    items = await page.query_selector_all('.item')
    results = []
    for item in items:
        title = await item.query_selector('.title')
        results.append({'title': await title.inner_text()})

    await Actor.push_data(results)
    await browser.close()
```

### Using Selenium

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

try:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'content'))
    )

    # Extract data
    items = driver.find_elements(By.CLASS_NAME, 'item')
    results = [{'title': item.find_element(By.CLASS_NAME, 'title').text}
               for item in items]

    await Actor.push_data(results)
finally:
    driver.quit()
```

## Proxy Management

```python
from apify import Actor
from apify_client import ApifyClient

async def main():
    async with Actor:
        # Get proxy configuration
        proxy_configuration = await Actor.create_proxy_configuration()

        # Use with httpx
        proxy_url = await proxy_configuration.new_url()
        async with httpx.AsyncClient(proxies={'all://': proxy_url}) as client:
            response = await client.get('https://example.com')
```

## Logging

```python
from apify import Actor

async def main():
    async with Actor:
        Actor.log.info('Processing started')
        Actor.log.debug('Debug information')
        Actor.log.warning('Warning message')
        Actor.log.error('Error occurred')

        # Structured logging
        Actor.log.info('Scraped items', extra={'count': 100})
```

## Configuration and Environment

```python
# Check if running on Apify platform
if Actor.is_at_home():
    Actor.log.info('Running on Apify')

# Access configuration
config = Actor.config
Actor.log.info(f'Actor ID: {config.actor_id}')
Actor.log.info(f'Run ID: {config.actor_run_id}')

# Environment variables
import os
api_key = os.getenv('MY_API_KEY')
```

## Error Handling

```python
try:
    actor_input = await Actor.get_input() or {}

    # Validate input
    if not actor_input.get('url'):
        raise ValueError('URL is required')

    # Process...

except Exception as e:
    Actor.log.error(f'Actor failed: {e}')
    await Actor.exit(exit_code=1)
```

## Performance and Memory

```python
# Process in batches to avoid memory issues
items = []
batch_size = 100

for i in range(1000):
    items.append({'index': i})

    if len(items) >= batch_size:
        await Actor.push_data(items)
        items = []

# Push remaining items
if items:
    await Actor.push_data(items)
```
