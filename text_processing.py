import re

def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove special characters
    return cleaned_text.strip()

def deduplicate_text(text_list):
    return list(dict.fromkeys(text_list))  # Remove duplicates while preserving order
