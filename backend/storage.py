import threading
import gphoto2 as gp
import json
import uuid
from utils import convert_arw_to_jpeg
import os
import time

class PhotoStorage:
    def __init__(self, folder='images', db='photos.json'):
        self.lock = threading.Lock()
        self.folder = folder
        self.db_path = f"{folder}/{db}"

        os.makedirs(self.folder, exist_ok=True)

        if not os.path.exists(self.db_path):
            self.db = {}
        else:
            with open(self.db_path, 'r') as f:
                self.db = json.load(f)


    def save(self, camera_file, file_path, simulated=None):
        photo_id = str(uuid.uuid4())
        path = f"{self.folder}/{photo_id}"
        ext = file_path.split('.')[-1]

        if simulated:
            with open(f"{path}.{ext}", "wb") as f:
                f.write(simulated)

        else:
            gp.check_result(gp.gp_file_save(camera_file, f"{path}.{ext}"))

        if ext == 'arw':
            convert_arw_to_jpeg(f"{path}.{ext}", f"{path}.jpeg")

        with self.lock:
            self.db[photo_id] = {
                'path': path,
                'ext': ext,
                'emails': [],
                'phones': [],
                'taken_at': int(time.time()),
                'promotional_consent': False,
            }

            with open(self.db_path, 'w+') as f:
                json.dump(self.db, f)

        return photo_id

    def get_photo_bytes(self, photo_id, ext="jpeg"):
        record = self.db.get(photo_id)
        if not record:
            return None

        with open(f"{record['path']}.{ext}", 'rb') as f:
            return f.read()

    def add_emails(self, photo_id, emails):
        with self.lock:
            self.db[photo_id]['emails'].extend(emails)

            with open(self.db_path, 'w+') as f:
                json.dump(self.db, f)

    def add_phone(self, photo_id, phones):
        with self.lock:
            self.db[photo_id]['phones'].extend(phones)

            with open(self.db_path, 'w+') as f:
                json.dump(self.db, f)

    # TODO: Add maybe QR code to photo to link to discord bot or something?
