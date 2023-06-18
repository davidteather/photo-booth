import cv2
import gphoto2 as gp
import numpy as np
from flask import Flask, Response, jsonify, request, abort
import threading
import os
from storage import PhotoStorage
from flask_bcrypt import Bcrypt
import logging
from dotenv import load_dotenv

ps = PhotoStorage()
app = Flask(__name__)
context = gp.Context()
camera = gp.Camera()
camera.init(context)
settings_lock = threading.Lock()
camera_lock = threading.Lock()
logger = logging.getLogger('werkzeug')
bcrypt = Bcrypt(app)
load_dotenv()

if not os.path.exists('images'):
    os.mkdir('images')

# Shared Password for all endpoints, goal is to prevent random people on same network from messing with the camera
# This isn't the most secure way to do this, but it's good enough for this project
HASHED_PASSWORD = bcrypt.generate_password_hash(os.getenv('APP_PASSWORD')).decode('utf-8')


@app.before_request
def check_password():
    # Check for password parameter in the URL
    password = request.args.get('password')
    if password is None or not bcrypt.check_password_hash(HASHED_PASSWORD, password):
        # Return a 401 status if password is incorrect or not provided
        abort(401)

'''TODO:
- Maybe take photo with RAW&JPEG 
  - Also evaluate if we even need RAW
    - Only reason I'd want RAW is if we wanted to manually post process the images
      after people take the photos
- Route to text/email image
    - Associate photo ID with the places it was sent to
    - Also opt-in to promotional materials
'''

def change_config(camera, config_name, config_value):
    with settings_lock:
        config = camera.get_config()
        target = config.get_child_by_name(config_name)
        target.set_value(config_value)
        camera.set_config(config)

def capture(camera, context):
    with camera_lock:
        change_config(camera, "imagequality", "RAW")
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
        camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, context))
        change_config(camera, "imagequality", "Standard")

    photo_id = ps.save(camera_file, file_path.name)
    b = ps.get_photo_bytes(photo_id, ext='jpeg')
    return {'photo_id': photo_id}

@app.route('/capture', methods=['POST'])
def take_photo():
    content = capture(camera, context)
    return jsonify(content)

@app.route('/photos/<photo_id>')
def get_photo(photo_id):
    return Response(ps.get_photo_bytes(photo_id, ext='jpeg'), mimetype='image/jpeg')

@app.route('/send', methods=['POST'])
def send_photo():
    content = request.json
    photo_ids = content['photo_ids']
    emails = content['emails']
    phones = content['phones']
    promotional_consent = content['promotional_consent']

    for photo_id in photo_ids:
        ps.add_emails(photo_id, emails)
        ps.add_phones(photo_id, phones)

    # TODO: Send emails and texts

    return jsonify({'success': True})

# Streaming/Preview
def capture_streaming_frame():
    with camera_lock:
        # Capture the preview
        camera_file = gp.check_result(gp.gp_camera_capture_preview(camera, context))
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

    # Convert the raw data to a numpy array and reshape for image display
    image = np.frombuffer(file_data, np.uint8)
    image = cv2.imdecode(image, 1)

    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', image)
    return img_encoded.tostring()

@app.route('/stream')
def stream():
    def generate():
        while True:
            frame = capture_streaming_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True, ssl_context=('./ssl/cert.pem', './ssl/key.pem'))

    change_config(camera, "imagesize", "Small")
    change_config(camera, "imagequality", "Standard")
