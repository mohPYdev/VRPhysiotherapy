import numpy as np
import mediapipe as mp
import pandas as pd
import cv2
import os 
###### Use model in video
#Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False,min_detection_confidence=0.5,min_tracking_confidence=0.5)

# Specify the directory path 
directory = 'Input_video/'

# List all files in the directory
files = os.listdir(directory)
header_list=['l_shoulder','r_shoulder','l_elbow','r_elbow','l_wrist','r_wrist','l_hip','r_hip']
df=pd.DataFrame(columns=header_list)
for file in files:
    if file.endswith('.mp4'):
        file_path = os.path.join(directory, file)

        # read video
        cap = cv2.VideoCapture(file_path)
        # cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Cannot open camera or file")
            exit()

        # Save output video
        output_video = f"Output_video/{file}_output.mp4"

        # Retrieve the input video properties and setup for output video
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

        while True:
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
                df.loc[len(df)] = landmarks_interest
            cv2.imshow('Frame', person_crop_in_RGB)
            video_writer.write(person_crop_in_RGB)
            if cv2.waitKey(1) == ord('q') or not ret:
                break
        
        df.to_csv(f"CSV/{file}.csv",index = False)

# When everything done, release the capture
cap.release()
video_writer.release()
cv2.destroyAllWindows()