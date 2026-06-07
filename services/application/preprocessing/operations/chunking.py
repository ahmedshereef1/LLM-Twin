import re

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)

from services.network import EmbeddingModelSingleton

embedding_model = EmbeddingModelSingleton()


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    charachter_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n"], chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    text_split_by_characters = charachter_splitter.split_text(text)

    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=chunk_overlap,
        tokens_per_chunk=embedding_model.max_input_length,
        model_name=embedding_model.model_id,
    )

    chunks_by_token = []
    for section in text_split_by_characters:
        chunks_by_token.extend(token_splitter.split_text(section))

    return chunks_by_token


def chunk_document(text: str, min_length: int, max_length: int) -> list[str]:
    """Alias for chunk_article()."""
    return chunk_article(text, min_length, max_length)


def chunk_article(text: str, min_length: int, max_length: int) -> list[str]:
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", text)

    extracts = []
    current_chunks = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current_chunks) + len(sentence) <= max_length:
            current_chunks += sentence + " "
        else:
            if len(current_chunks) >= min_length:
                extracts.append(current_chunks.strip())
            current_chunks = sentence + " "

    if len(current_chunks) >= min_length:
        extracts.append(current_chunks.strip())

    return extracts
