import threading
import eel
import cv2
import time
from config import Config
from PIL import Image
import google.generativeai as gai
import os
import base64

gai.configure(api_key=Config['API-KEY'])
model = gai.GenerativeModel("gemini-1.5-flash")
eel.init('web')

# Capture video 
camera = cv2.VideoCapture(0)

def get_video_frame():
    ret, frame = camera.read()
    if not ret:
        return None
    return frame

# @eel.expose
# def get_frame():
#     frame = get_video_frame()
#     if frame is not None:
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_data = base64.b64encode(buffer).decode('utf-8')
#         return f"data:image/jpeg;base64,{frame_data}"
#     return None

# Function to video feed
def vision():
    while True:
        frame = get_video_frame()
        if frame is not None:
            cv2.imshow("Video Feed", frame)
        else:
            print("Failed to decode frame.")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        time.sleep(0.03)

@eel.expose
def process_command(command: str):
    frame = get_video_frame()  # Capture the current frame
    if frame is not None:
        response = process_frame_with_gemini(frame, command)
        return response
    return "Failed to capture frame."

def process_frame_with_gemini(frame, data:str):
    if data.lower().startswith("Avish"):
        cv2.imwrite("sample.jpg", frame)
        img = Image.open("sample.jpg")
        response = model.generate_content([img, data])
        os.remove('sample.jpg')
        return response.text
    else:
        response = model.generate_content(data)
        return response.text

# Start the video feed and command input in separate threads
threading.Thread(target=vision, daemon=True).start()
# threading.Thread(target=process_command, daemon=True).start()
eel.start('index.html', size=(800, 600))
camera.release()
cv2.destroyAllWindows()
