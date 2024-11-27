import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio_file = "extracted_audio.wav"
    video.audio.write_audiofile(audio_file)
    return audio_file

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # Read the entire audio file
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Audio not understood"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def summarize_text(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(filtered_words)
    most_common = word_freq.most_common(10)  # Get the 5 most common words
    return most_common

def main(video_file):
    audio_file = extract_audio(video_file)
    transcript = transcribe_audio(audio_file)
    summary = summarize_text(transcript)

    print("Transcript:")
    print(transcript)
    print("\nSummary (Most Common Words):")
    for word, freq in summary:
        print(f"{word}: {freq}")

if __name__ == "__main__":
    video_file = "C:\\Users\\Krishna kumar\\Videos\\C for loops 🔁 - Bro Code (1080p, h264, youtube).mp4" # Replace with your video file path
    main(video_file)