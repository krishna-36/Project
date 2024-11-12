from transformers import pipeline

def summarize_text(text_data):
    summarizer = pipeline("summarization")
    full_text = " ".join(text_data)
    summary = summarizer(full_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
