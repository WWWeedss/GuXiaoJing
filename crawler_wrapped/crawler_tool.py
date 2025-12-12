import asyncio
from crawl4ai import AsyncWebCrawler


def fetch_url_markdown(url: str, max_retries: int = 10, initial_delay: float = 1.0) -> str:
    """
    使用 Crawl4AI 异步抓取网页并返回 Markdown 内容，支持自动重试。

    Args:
        url: 要抓取的 URL
        max_retries: 最大重试次数（默认 10）
        initial_delay: 初始重试延迟（秒），后续按指数退避（默认 1 秒）

    Returns:
        网页的 Markdown 内容

    Raises:
        RuntimeError: 如果所有重试都失败
    """

    async def _fetch_with_retry():
        for attempt in range(max_retries + 1):
            try:
                async with AsyncWebCrawler(
                        browser_args=["--no-sandbox", "--disable-setuid-sandbox"]
                ) as crawler:
                    result = await crawler.arun(
                        url=url,
                        timeout=90,  # 延长超时时间（秒）
                        wait_for="body"  # 确保 DOM 加载
                    )
                    if result.success:
                        return result.markdown
                    else:
                        raise RuntimeError("Crawl result marked as not successful")

            except Exception as e:
                # 判断是否是可重试的错误
                error_str = str(e).lower()
                is_timeout = "timeout" in error_str or "timed out" in error_str
                is_navigate_fail = "failed on navigating" in error_str

                if attempt < max_retries and (is_timeout or is_navigate_fail):
                    delay = initial_delay * (2 ** attempt)  # 指数退避：1s, 2s, 4s, 8s...
                    print(f"[RETRY {attempt + 1}/{max_retries}] Failed to fetch {url}: {e}")
                    print(f"  → Retrying in {delay:.1f} seconds...")
                    await asyncio.sleep(delay)
                    continue
                else:
                    # 最后一次失败或不可重试的错误
                    raise RuntimeError(f"Failed to fetch {url} after {max_retries + 1} attempts: {e}") from e

        raise RuntimeError("Unexpected state: retry loop exited without success or exception")

    return asyncio.run(_fetch_with_retry())