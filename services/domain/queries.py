from pydantic import UUID4, Field

from services.domain.base import VectorBaseDocument
from services.enums.document_type import DataCategory


class Query(VectorBaseDocument):
    content: str
    author_id: UUID4 | None = None
    author_user_name: str | None = None
    metadata: dict = Field(default_factory=dict)

    class Config:
        category = DataCategory.QUERIES

    @classmethod
    def form_str(cls, query: str) -> "Query":
        return Query(content=query.strip("\n "))

    def replace_content(self, new_content: str) -> "Query":
        return Query(
            id=self.id,
            content=new_content,
            author_id=self.author_id,
            author_user_name=self.author_user_name,
            metadata=self.metadata,
        )


class EmbeddedQuery(Query):
    embedding: list[float]

    class Config:
        category = DataCategory.QUERIES
