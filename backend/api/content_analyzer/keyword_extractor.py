from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# MiniLM lightweight model
_model = SentenceTransformer("all-MiniLM-L6-v2")
_kw_model = KeyBERT(model=_model)


def extract_keywords_keybert(text: str, top_k: int = 10):
    """
    Extract highly relevant keywords using KeyBERT + MiniLM embeddings.
    """
    if not text or len(text.strip()) == 0:
        return []

    keywords = _kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_k=top_k,
        highlight=False
    )

    # Return only the keyword text
    return [kw[0] for kw in keywords]
