import cv2
import os

def extract_frames(video_path, interval=1, output_folder="frames"):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    success, frame = cap.read()
    while success:
        if frame_count % interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
        frame_count += 1
        success, frame = cap.read()
    cap.release()
    return output_folder
