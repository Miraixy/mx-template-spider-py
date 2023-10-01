from src.models.urls import DB_Url
from src.utils import X_Finder

from .base import WebsiteBase


class TargetWebsite(WebsiteBase):
    def check_item_url(self, url: DB_Url, xf: X_Finder):
        return True

    def crawl_item_url(self, url: DB_Url, xf: X_Finder):
        ...
