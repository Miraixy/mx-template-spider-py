import asyncio

from src.utils import (
    X_Finder,
    async_fetch,
    get_url_domain,
    get_url_path,
    reduce_url,
)


async def main():
    url = "https://www.lookick.ru/"

    print(f"domain: {get_url_domain(url)}")
    print(f"path: {get_url_path(url)}")
    print(f"reduced url: {reduce_url(url)}")
    # print(f"fetch url: {(await async_fetch(url))[:100]}...")

    xf = X_Finder(await async_fetch(url))
    print(f"all urls: {xf.get_all_url()}")

def start():
    asyncio.run(main())
