import websocket
import threading
import numpy as np
import mediapipe as mp
import pandas as pd
import cv2

header_list=['l_shoulder','r_shoulder','l_elbow','r_elbow','l_wrist','r_wrist','l_hip','r_hip']
data=pd.DataFrame(columns=header_list)

locked = False

def ML_calculation(ws):
    global data
    global locked

    #Initialize mediapipe pose class.
    mp_pose = mp.solutions.pose
    # Initializing mediapipe drawing class, useful for annotation.
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(static_image_mode=False,min_detection_confidence=0.5,min_tracking_confidence=0.5)
    # read video
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera or file")
        exit()
        
    # Save output video
    output_video = f"Output_video/output.mp4"

    # Retrieve the input video properties and setup for output video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, frame_size)
        
    header_list=['l_shoulder','r_shoulder','l_elbow','r_elbow','l_wrist','r_wrist','l_hip','r_hip']
    local_data=pd.DataFrame(columns=header_list)
    
    while (True):
        
        if not locked:
            locked = True
            data = local_data.copy()
            locked = False
        
        landmarks_interest=[]
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        person_crop_in_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detection
        pose_result = pose.process(person_crop_in_RGB)
        person_crop_in_RGB=cv2.cvtColor(person_crop_in_RGB,cv2.COLOR_RGB2BGR)
        if pose_result.pose_landmarks:
            landmarks = pose_result.pose_landmarks.landmark
        else:
            landmarks=0
            
        if landmarks:
            # draw landmarks in frame
            mp_drawing.draw_landmarks(image=person_crop_in_RGB, landmark_list=pose_result.pose_landmarks,
                                connections=mp_pose.POSE_CONNECTIONS)
            mediapipe_landmarks=[[landmark.x,landmark.y,landmark.z] for landmark in landmarks]
            landmarks_interest = [mediapipe_landmarks[11],mediapipe_landmarks[12],mediapipe_landmarks[13],mediapipe_landmarks[14],mediapipe_landmarks[15],mediapipe_landmarks[16],mediapipe_landmarks[23],mediapipe_landmarks[24]]
            local_data.loc[len(local_data)] = landmarks_interest
        cv2.imshow('Frame', person_crop_in_RGB)
        video_writer.write(person_crop_in_RGB)
        if cv2.waitKey(1) == ord('q') or not ret:
            break
    
    print(local_data)
    # When everything done, release the capture
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()


def run_ml_calculation(ws):
    ml_thread = threading.Thread(target=ML_calculation, args=(ws,))
    ml_thread.start()

def on_message(ws, message):
    print("Received message from server:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, x, y):
    print("Connection closed")

def on_open(ws):
    print("Connected to server!")

    # Start ML calculation in a separate thread
    run_ml_calculation(ws)

if __name__ == "__main__":
    # WebSocket client
    ws = websocket.WebSocketApp("ws://localhost:8080",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.on_open = on_open
    
    # Run the WebSocket client
    ws.run_forever()

    ML_calculation(ws)