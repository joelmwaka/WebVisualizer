import cv2
import time
import numpy as np
from collections import deque
from flask import Flask, render_template, Response

path_to_templates = "C:/Users/joelm/Desktop/Portfolio/Projects/WebVisualizer/webvisualizer/templates/"
app = Flask(__name__)
app.template_folder = path_to_templates
frames = deque(maxlen=10)
display_frame = None

@app.route('/')
def index():
    return render_template('index.html')


def send_frame(frame):

    global frames
    frames.append(frame)


def get_frames():

    global frames
    
    if frames:
        display_frame = frames.popleft()
        return cv2.imencode('.jpg', display_frame)[1].tobytes()
    else:
        if display_frame is not None:
            return cv2.imencode('.jpg', display_frame)[1].tobytes()
        else:
            color = (200, 200, 200)
            height = 480
            width = 640
            default_frame = np.full((height, width, 3), color, dtype=np.uint8)
            return cv2.imencode('.jpg', default_frame)[1].tobytes()


def generate():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + get_frames() + b'\r\n')
        time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/left_button')
def left_button():
    pass
    return render_template("index.html")


@app.route('/right_button')
def right_button():
    pass
    return render_template("index.html")

