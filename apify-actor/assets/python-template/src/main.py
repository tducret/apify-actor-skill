"""
Apify Actor - Main entry point
"""

import asyncio
from datetime import UTC, datetime

from apify import Actor


async def main():
    """
    Main actor function
    """
    async with Actor:
        # Get input from the actor's default key-value store
        actor_input = await Actor.get_input() or {}

        # Log the input
        Actor.log.info("Actor input:", extra={"input": actor_input})

        # TODO: Implement your actor logic here
        # Example: Extract configuration from input
        start_url = actor_input.get("startUrl", "https://example.com")
        max_items = actor_input.get("maxItems", 10)

        Actor.log.info(f"Processing URL: {start_url}")

        # TODO: Process the input and extract data
        # Example: Push results to dataset
        results = []
        for i in range(max_items):
            results.append(
                {"index": i, "url": start_url, "timestamp": datetime.now(UTC).isoformat()}
            )

        # Push data to the default dataset
        await Actor.push_data(results)

        Actor.log.info(f"Successfully processed {len(results)} items")


if __name__ == "__main__":
    asyncio.run(main())
