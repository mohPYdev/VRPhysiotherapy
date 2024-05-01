import websocket
import threading
import numpy as np
import mediapipe as mp
import pandas as pd
import cv2
import os

# Initialize MediaPipe pose class and drawing class
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

ml_thread = None

# Initialize recording variables
recording     = False
landmark_data = []


def start_recording():
    global recording
    recording = True
    print("Starting recording...")
    # Initialize video capture and pose detection
    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    while recording:
        ret, frame = cap.read()
        if not ret:
            break
        person_crop_in_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_result = pose.process(person_crop_in_RGB)
        if pose_result.pose_landmarks:
            landmarks = pose_result.pose_landmarks.landmark
            landmark_data.append([landmark.x, landmark.y, landmark.z] for landmark in landmarks)
        cv2.imshow('Frame', person_crop_in_RGB)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def finish_recording():
    global recording
    recording = False
    print("Finishing recording...")
    # Save landmark data to CSV file
    print(landmark_data)
    df = pd.DataFrame(landmark_data, columns=['x', 'y', 'z'])
    df.to_csv('landmark_data.csv', index=False)
    print('saved!')
    # Run main.py script in anomaly_detection folder
    # os.system('python main.py')
    
def run_ml_calculation(ws):
    global ml_thread
    ml_thread = threading.Thread(target= start_recording)
    ml_thread.start()

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, x, y):
    print("Connection closed")

    
def on_message(ws, message):
    print("Received message from server:", message)
    if message == "Start":
        run_ml_calculation(ws)
    elif message == "End":
        finish_recording()

def on_open(ws):
    print("Connected to server!")
    
    

if __name__ == "__main__":
    
    # Initialize WebSocket client
    ws = websocket.WebSocketApp("ws://localhost:8080",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()