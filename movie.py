from moviepy.editor import VideoFileClip

def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio_file = "extracted_audio.wav"
    video.audio.write_audiofile(audio_file)
    return audio_file