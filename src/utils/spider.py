from lxml import etree


class X_Finder:
    def __init__(self, raw_html: str):
        self.raw_html = raw_html
        self.dom = etree.HTML(self.raw_html, parser=etree.HTMLParser())

    def lxml_x_match(self, x_path: str, attr="", limit=256) -> list[str]:
        """从页面提取所有符合xpath规则的元素字符串"""

        def quick_value(ls: list, alternative_value="") -> str:
            """快速列表取值"""
            if len(ls) == 0:
                return alternative_value
            return ls[0].strip() if (ls[0] and ls[0].strip()) else alternative_value

        try:
            res_list = []
            for i in range(1, limit + 1):
                try:
                    tags = self.dom.xpath(x_path.format(i))
                    if attr:
                        if attr.lower() == "html":  # 获取元素下的 HTML 文本
                            res_list += [etree.tostring(x, method="html", encoding="unicode") for x in tags]  # type: ignore
                        else:
                            res_list += [x.get(attr) for x in tags]
                    else:  # 获取元素下的普通文本
                        res_list += [
                            x.text or quick_value(x.xpath("./text()")) for x in tags
                        ]
                except:
                    break
                if "{}" not in x_path:  # 如果不需要自动递增
                    break
            return res_list  # noqa: TRY300
        except:
            return []

    def get_all_url(self) -> list[str]:
        """获取页面所有链接"""

        try:
            return self.dom.xpath("//a/@href")[:8192]
        except:
            return []
