import cv2
import gphoto2 as gp
import numpy as np
from flask import Flask, Response, jsonify

app = Flask(__name__)
context = gp.Context()
camera = gp.Camera()
camera.init(context)

'''TODO:
- Global lock for camera settings
- Capture image associating with ID locally
    - Convert RAW to JPEG
    - Save to local directory
    - Return an ID of the image to the frontend
- Route to text/email image
    - Associate photo ID with the places it was sent to
    - Also opt-in to promotional materials
'''

def change_config(camera, config_name, config_value):
    config = camera.get_config()
    target = config.get_child_by_name(config_name)
    target.set_value(config_value)
    camera.set_config(config)

def capture(camera, context):
    change_config(camera, "imagequality", "RAW")
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
    camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(camera_file, file_path.name))
    change_config(camera, "imagequality", "Standard")
    return f'Captured and saved image at: {file_path.name}'

@app.route('/capture', methods=['POST'])
def take_photo():
    change_config(camera, "imagesize", "Large")
    message = capture(camera, context)
    return jsonify({'message': message})

def capture_streaming_frame():
    change_config(camera, "imagesize", "Small")
    change_config(camera, "imagequality", "Standard")

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
    app.run(host='0.0.0.0', port=8000, threaded=True)
