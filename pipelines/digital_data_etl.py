from zenml import pipeline

from scripts.etl import crawl_links, get_or_create_user


@pipeline
def digial_data_etl(user_name: str, links: list[str]) -> str:
    user = get_or_create_user(user_name)
    last_step = crawl_links(user=user, links=links)

    return last_step.invocation_id
