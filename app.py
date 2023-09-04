import os
import vlc
import time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ensure 'uploads' directory exists
uploads_dir = 'uploads'
os.makedirs(uploads_dir, exist_ok=True)

# Global variables to store video information
video_path = ""
player = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global video_path, player

    # Get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        # Save the uploaded file to a temporary directory
        video_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(video_path)

        # Create a VLC media player instance, set to full-screen, and play the video
        player = vlc.MediaPlayer(video_path)
        player.set_fullscreen(True)  # Enable full screen
        player.play()

    return redirect(url_for('index'))

@app.route('/play', methods=['GET'])
def play():
    global player

    if player is not None:
        player.play()
        return "Playing"
    return "No video selected"

@app.route('/pause', methods=['GET'])
def pause():
    global player

    if player is not None:
        player.pause()
        return "Paused"
    return "No video selected"

@app.route('/stop', methods=['GET'])
def stop():
    global player

    if player is not None:
        player.stop()
        return "Stopped"
    return "No video selected"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
