import json

import aiohttp

from src.log import logger


def drop_empty_from_list(lst: list) -> list[str]:
    """去除列表中的空字符串元素"""

    return [i for i in lst if i.strip()]


def split_and_drop_empty(s: str, sep: str) -> list[str]:
    """切割字符串并去除空字符串元素"""
    return [i.strip() for i in s.split(sep) if i.strip()]


async def async_fetch(url) -> str:
    """异步获取网页"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    async with aiohttp.ClientSession(headers=headers) as session:  # noqa: SIM117
        async with session.get(url) as resp:
            return await resp.text()


def retry(func, retry_times=3):
    """重试装饰器"""

    def wrapper(*args, **kwargs):
        for _ in range(retry_times):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"重试 {func.__name__} 函数失败 | {e}")
                raise
        return None

    return wrapper


def safe_int(s, default=-1) -> int:
    """不会报错的int转换"""
    try:
        return int(s)
    except:
        return default


def json_list_stringify_limit(lst: list, limit=1024) -> str:
    """列表转json列表长度自动限制(丢弃超出限制的元素)"""
    while True:
        if len(lst) < 1:
            return "[]"
        res = json.dumps(lst)
        if len(res) <= limit:
            return res
        lst = lst[:-1]


def quick_value(ls: list, alternative_value="") -> str:
    """快速列表取值"""
    if len(ls) == 0:
        return alternative_value
    return ls[0].strip() if (ls[0] and ls[0].strip()) else alternative_value


def get_url_domain(url: str) -> str:
    try:
        return url.split("//")[1].split("/")[0]
    except:
        return ""


def get_url_path(url: str) -> str:
    return "/" + url.split("//")[1].split("/")[1]


def reduce_url(url: str) -> str:
    """去除url中的锚点"""
    if url.startswith("#"):
        return ""
    return url.split("#")[0]


def is_relative_url(url: str) -> bool:
    return url.startswith(("/", "#"))
