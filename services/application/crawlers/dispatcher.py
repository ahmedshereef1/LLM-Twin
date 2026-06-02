from loguru import logger

import re
from urllib.parse import urlparse

from .base_selenium_crawler import BaseCrawler
from .github import GithubCrawler
from .custom_article import CustomArticleCrawler
from .linkedin import LinkedinCrawler
from .medium import MediumCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers = {}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        dispatcher = cls()

        return dispatcher

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        parsed_domain = urlparse(domain)
        domain = parsed_domain.netloc

        self._crawlers[r"https://(www\.)?{}/*".format(re.escape(domain))] = crawler

    def register_medium(self) -> "CrawlerDispatcher":
        self.register("https://medium.com", MediumCrawler)

        return self

    def register_linkedin(self) -> "CrawlerDispatcher":
        self.register("https://linkedin.com", LinkedinCrawler)

        return self

    def register_github(self) -> "CrawlerDispatcher":
        self.register("https://github.com", GithubCrawler)

        return self

    def get_crawler(self, url: str) -> BaseCrawler:
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()

        logger.warning(
            f"No crawler found for {url}. Defaulting to CustomArticleCrawler."
        )
        return CustomArticleCrawler
