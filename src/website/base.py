from typing import Generator

from src.models.urls import DB_Url
from src.utils import X_Finder


class WebsiteBase:
    def iter_urls(self) -> Generator[DB_Url, None, None]:
        while True:
            urls = DB_Url.get_available(limit=100)
            if len(urls) == 0:
                break
            for url in urls:
                yield url
        return

    def check_item_url(self, url: DB_Url, xf: X_Finder):
        raise NotImplementedError

    def crawl_item_url(self, url: DB_Url, xf: X_Finder):
        raise NotImplementedError
