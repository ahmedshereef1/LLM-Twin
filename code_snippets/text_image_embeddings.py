from sentence_transformers import SentenceTransformer

from PIL import Image

if __name__ == "__main__":
    image = Image.open(r"data\images\German-Shepherd.png")

    # Load the model
    model = SentenceTransformer("clip-ViT-B-32")

    # Encode the loaded image
    image_emb = model.encode(image)

    # Encode text description
    text_emb = model.encode(
        [
            "A german dog smiling.",
            "A German Shepherd dog with a black and tan coat, standing outdoors, alert and intelligent.",
            "A man eating in the garden.",
        ]
    )
    print(text_emb.shape)

    # Compute similarities.
    similarity_scores = model.similarity(image_emb, text_emb)
    print(similarity_scores)
