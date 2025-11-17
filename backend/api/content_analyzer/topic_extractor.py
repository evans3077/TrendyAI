from sentence_transformers import SentenceTransformer, util
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_topics_minilm(text: str, num_topics: int = 5):
    """
    Generate semantic topics using MiniLM sentence embeddings + clustering.
    """

    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 15]
    if len(sentences) < 3:
        return []

    embeddings = _model.encode(sentences, convert_to_tensor=True)

    # Compute sentence similarity matrix
    sim_matrix = util.cos_sim(embeddings, embeddings)

    # Pick top-N diverse sentences as topics
    topic_indices = util.semantic_search(
        query_embeddings=embeddings.mean(axis=0, keepdims=True),
        corpus_embeddings=embeddings,
        top_k=num_topics
    )[0]

    topics = []
    for hit in topic_indices:
        idx = hit["corpus_id"]
        topics.append(sentences[idx])

    return topics
