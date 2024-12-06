from flask import Flask, request, render_template, jsonify
import os
from VideoSummarizer import summarize_video  # Import your summarization function

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to render HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle video upload and summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400

    video_file = request.files['video']
    
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded video
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)

    # Perform video summarization (assuming your summarization function is implemented in `summarize_video`)
    summary, full_transcript = summarize_video(video_path)

    # Return both the summary and full transcript
    return jsonify({
        'summary': summary,
        'full_transcript': full_transcript
    })

if __name__ == '__main__':
    app.run(debug=True)
