import asyncio
import time

from src.conf import config
from src.log import logger
from src.models.urls import DB_Url
from src.utils import (
    X_Finder,
    async_fetch,
    get_url_domain,
    is_relative_url,
    reduce_url,
    retry,
)
from src.utils.db import database_init
from src.website.website import TargetWebsite

tw = TargetWebsite()
ALLOW_DOMAIN = "*" if config.ALLOW_CORS else get_url_domain(config.ENTRY_URL)

def finish_url(url: DB_Url, reason: str = ""):
    reason = reason[:1024]  # 限制长度
    DB_Url.update(
        url,
        task_finished=True,
        output=reason,
    )

@retry
async def deal_url(origin_url: DB_Url | str):
    """处理 url"""
    if isinstance(origin_url, str):
        url: DB_Url | None = DB_Url.get_by_url(reduce_url(origin_url))
        if url is None:
            url = DB_Url(value=origin_url)
            DB_Url.add(url)
    else:
        url = origin_url

    domain = get_url_domain(str(url.value))

    # 域名检查
    if ALLOW_DOMAIN != "*" and domain != ALLOW_DOMAIN:
        finish_url(url, f"域名: {domain} 不在允许范围内")
        return

    logger.info(f"开始处理 url: {url.value}...")

    xf = X_Finder(await async_fetch(str(url.value)))
    new_urls = xf.get_all_url()

    # 获取所有当前页面链接的 url
    for u in [u for u in new_urls if u.strip()]:
        _domain = get_url_domain(u)
        # 跳过无法解析的域名
        if not _domain:
            continue
        # 相对路径处理
        if is_relative_url(u):
            u = f"{url.value}{u}"
        # 重复检查
        if u == str(url.value):
            continue

        if DB_Url.get_by_url(str(u)) is None:
            DB_Url.add(DB_Url(value=u, domain=_domain))

    if tw.check_item_url(url, xf):
        # 开始爬取页面信息
        tw.crawl_item_url(url, xf)

    finish_url(url, "爬取完成")

    sta = time.time()
    logger.info(f"爬取 url: {url.value} 完成 | 页面 url 数量: {len(new_urls)} | 耗时: {time.time() - sta}s")


async def main():
    try:
        database_init()
    except Exception as e:
        logger.error(f"数据库初始化失败 | 错误: {e}")
        exit(1)

    # 初始爬取
    await deal_url(config.ENTRY_URL)

    task_list: list[asyncio.Task] = []

    for url in tw.iter_urls():  # 迭代所有可爬取的 url
        try:
            task = asyncio.create_task(deal_url(url))
            task_list.append(task)
        except Exception as e:
            finish_url(url, f"爬取 url: {url} 失败 | 错误: {e}")
            logger.error(f"爬取 url: {url} 失败 | 错误: {e} / 跳过...")

        while len(task_list) > config.MAX_CONNECTIONS:
            await asyncio.sleep(0.1)
            task_list = [t for t in task_list if not t.done()]

    logger.success("爬取队列为空，结束爬取!")


def start():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("手动中断...")


if __name__ == "__main__":
    start()
