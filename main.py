import os
from video_processing import extract_frames
from text_detection import perform_ocr
from text_processing import clean_text, deduplicate_text
from summarization import summarize_text

def main(video_path):
    print("Extracting frames...")
    frames_folder = extract_frames(video_path)

    print("Performing OCR on frames...")
    raw_text_data = perform_ocr(frames_folder)

    print("Cleaning text data...")
    cleaned_text_data = [clean_text(text) for text in raw_text_data]
    unique_text_data = deduplicate_text(cleaned_text_data)

    print("Summarizing text...")
    summary = summarize_text(unique_text_data)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ")
    main(video_path)
