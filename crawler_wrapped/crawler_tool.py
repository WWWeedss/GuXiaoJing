def fetch_url_markdown(url: str) -> str:
    import asyncio
    from crawl4ai import AsyncWebCrawler

    async def main():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown

    return asyncio.run(main())