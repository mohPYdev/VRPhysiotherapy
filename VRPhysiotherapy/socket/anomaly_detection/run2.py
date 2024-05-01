import websocket
import os
import csv
import mediapipe as mp
import cv2
import threading

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

recording = False
data = []

def start_recording():
    global recording
    recording = True
    print("Recording started.")

def finish_recording():
    global recording, data
    recording = False
    print("Recording finished.")

    # Save the results in a csv file
    output_folder = "anomaly_detection/results"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "body_landmarks.csv")

    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['l_shoulder', 'r_shoulder', 'l_elbow', 'r_elbow', 'l_wrist', 'r_wrist', 'l_hip', 'r_hip'])
        csv_writer.writerows(data)

    print(f"Results saved in {output_file}")

    # Run the main.py script in the anomaly_detection folder
    os.system("python anomaly_detection/main.py")

    data.clear()

def on_message(ws, message):
    if message == "Start":
        start_recording()
    elif message == "End":
        finish_recording()

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connected to server!")

if __name__ == "__main__":
    # WebSocket client
    ws = websocket.WebSocketApp("ws://localhost:8080",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Start the WebSocket client in a separate thread
    ws.run_forever(dispatcher=threading.Thread)
    wst = threading.Thread(target= ws.run_forever)
    wst.daemon = True
    wst.start()

    # Initialize MediaPipe pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe pose
        results = pose.process(frame_rgb)

        if results.pose_landmarks and recording:
            # Extract the body landmarks of interest
            landmarks = results.pose_landmarks.landmark
            landmarks_of_interest = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST],
                landmarks[mp_pose.PoseLandmark.RIGHT_WRIST],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            ]

            # Convert landmarks to string format
            landmarks_str = [f"[{lm.x}, {lm.y}, {lm.z}]" for lm in landmarks_of_interest]
            data.append(landmarks_str)

        # Draw the pose landmarks on the frame
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the frame
        cv2.imshow('MediaPipe Pose', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()