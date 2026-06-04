from sentence_transformers import SentenceTransformer


if __name__ == "__main__":
    model = SentenceTransformer("hkunlp/instructor-base")

    sentence = "Building LLM Applications from Scratch"

    instruction = (
        "Represent the title of a technical tutorial about large language models:"
    )

    embeddings = model.encode([[instruction, sentence]])
    print(embeddings.shape)
