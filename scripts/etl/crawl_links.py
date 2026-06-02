from loguru import logger
from tqdm import tqdm
from typing_extensions import Annotated
from urllib.parse import urlparse

from zenml import step, get_step_context

from services.domain.documents import UserDocument
from services.application.crawlers.dispatcher import CrawlerDispatcher


@step
def crawl_links(
    user: UserDocument, links: list[str]
) -> Annotated[list[str], "crawl_links"]:
    dispatcher = (
        CrawlerDispatcher.build()
        .register_substack()
        .register_linkedin()
        .register_medium()
        .register_github()
    )

    logger.info(f"Start crawling {len(links)} link(s).")

    metadata = {}
    successfull_crawls = 0
    for link in tqdm(links):
        successfull_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
        successfull_crawls += successfull_crawl

        metadata = _add_to_metadata(metadata, crawled_domain, successfull_crawl)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="crawl_links", metadata=metadata)

    logger.info(f"Successfully crawled {successfull_crawls} / {len(links)} links.")

    return links


def _crawl_link(
    dispatcher: CrawlerDispatcher, link: str, user: UserDocument
) -> tuple[bool, str]:
    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:
        crawler.extract(link=link, user=user)

        return (True, crawler_domain)
    except Exception as e:
        logger.error(f"An error occurred while crowling: {e!s}")

        return (False, crawler_domain)


def _add_to_metadata(metadata: dict, domain: str, successfull_crawl: bool) -> dict:
    if domain not in metadata:
        metadata[domain] = {}
    metadata[domain]["successful"] = (
        metadata[domain].get("successful", 0) + successfull_crawl
    )
    metadata[domain]["total"] = metadata[domain].get("total", 0) + 1

    return metadata
