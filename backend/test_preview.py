import cv2
import gphoto2 as gp
import numpy as np
import subprocess
import io

def change_config(camera, config_name, config_value):
    config = camera.get_config()
    target = config.get_child_by_name(config_name)
    target.set_value(config_value)
    camera.set_config(config)

def capture(camera):
    camera_file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
    camera_file = gp.check_result(gp.gp_camera_file_get(camera, camera_file_path.folder, camera_file_path.name, gp.GP_FILE_TYPE_NORMAL))
    return gp.check_result(gp.gp_file_get_data_and_size(camera_file))

def main():
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))

    # Create a context for the camera
    context = gp.Context()
    camera = gp.Camera()
    camera.init(context)

    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)

    change_config(camera, "imagesize", "Small")
    change_config(camera, "imagequality", "Standard")

    try:
        while True:
            # Capture the preview
            camera_file = gp.check_result(gp.gp_camera_capture_preview(camera, context))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

            # Convert the raw data to a numpy array and reshape for image display
            image = np.frombuffer(file_data, np.uint8)
            image = cv2.imdecode(image, 1)

            # Display the image
            cv2.imshow("Preview", image)

            # Check if spacebar is pressed
            if cv2.waitKey(1) & 0xFF == ord(' '):
                # Increase Resolution
                change_config(camera, "imagequality", "RAW")
                #change_config(camera, "imagesize", "Large") # if we're shooting in raw, don't think we need this bc it's JPEG size

                # Wait 3 seconds
                cv2.waitKey(3000)

                # Capture high quality image
                file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, context))
                print('Captured image at:', file_path)

                # Download the image
                camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, context))
                gp.check_result(gp.gp_file_save(camera_file, file_path.name))
                print('Image saved as:', file_path.name)

                # Lower Resolution Again
                change_config(camera, "imagesize", "Small")
                #change_config(camera, "imagequality", "Standard")

            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera
        cv2.destroyAllWindows()
        camera.exit(context)

if __name__ == "__main__":
    main()
