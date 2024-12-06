import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.effects import normalize, high_pass_filter, low_pass_filter
import whisper

def extract_audio_from_video(video_path, audio_path):
    """
    Extract audio from the video and save it as a WAV file.
    """
    print("Extracting audio from video...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    print(f"Audio extracted and saved to {audio_path}")

def enhance_audio(input_path, output_path):
    """
    Preprocess and enhance audio quality.
    """
    print("Enhancing audio...")
    audio = AudioSegment.from_file(input_path)
    audio = normalize(audio)  # Normalize volume
    audio = high_pass_filter(audio, cutoff=200)  # Reduce low-frequency noise
    audio = low_pass_filter(audio, cutoff=3000)  # Reduce high-frequency noise
    audio.export(output_path, format="wav")
    print(f"Audio enhanced and saved to {output_path}")

def split_audio(input_path, chunk_length_ms=30000):
    """
    Split audio into smaller chunks for better transcription.
    """
    print("Splitting audio into smaller chunks...")
    audio = AudioSegment.from_file(input_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    chunk_paths = []
    for idx, chunk in enumerate(chunks):
        chunk_path = f"chunk_{idx}.wav"
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)
    print(f"Audio split into {len(chunk_paths)} chunks.")
    return chunk_paths

def transcribe_with_whisper(audio_path):
    """
    Use Whisper to transcribe audio.
    """
    print("Transcribing with Whisper...")
    model = whisper.load_model("base")  # You can use "tiny", "small", "medium", or "large"
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_text(text):
    """
    Summarize the transcribed text using frequency-based summarization.
    """
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk.probability import FreqDist
    import nltk

    # Ensure NLTK data is available
    nltk.download("punkt")
    nltk.download("stopwords")

    print("Summarizing text...")
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Frequency distribution of words
    word_frequencies = FreqDist(filtered_words)
    max_frequency = max(word_frequencies.values(), default=1)
    normalized_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in normalized_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = 0
                sentence_scores[sentence] += normalized_frequencies[word]

    # Select top sentences for the summary
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:15]
    return " ".join(summary_sentences)

def summarize_video(video_path):
    """
    Summarize a video by extracting audio, transcribing it, and summarizing the transcript.
    """
    raw_audio_path = "temp_audio.wav"
    enhanced_audio_path = "enhanced_audio.wav"

    # Extract and enhance audio
    extract_audio_from_video(video_path, raw_audio_path)
    enhance_audio(raw_audio_path, enhanced_audio_path)

    # Split audio and transcribe
    audio_chunks = split_audio(enhanced_audio_path)
    full_transcript = ""
    for chunk in audio_chunks:
        transcript = transcribe_with_whisper(chunk)
        full_transcript += transcript + " "
        os.remove(chunk)  # Clean up chunk files

    # Summarize the transcript
    if full_transcript.strip():
        summary = summarize_text(full_transcript)
    else:
        summary = "No significant text could be transcribed from the video."

    return summary, full_transcript

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ").strip()

    try:
        summary, full_transcript = summarize_video(video_path)
        print("\nVideo Summary:")
        print(summary)
        print("\nFull Transcript:")
        print(full_transcript)
    except Exception as e:
        print(f"An error occurred: {e}")
