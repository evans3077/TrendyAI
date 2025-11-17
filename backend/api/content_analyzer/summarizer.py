from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1
)

def generate_summary(text: str) -> str:
    if len(text.strip()) < 50:
        return text

    summary = summarizer(
        text,
        max_length=180,
        min_length=60,
        do_sample=False
    )[0]["summary_text"]

    return summary.strip()
