from ultralytics import YOLO
import numpy as np
import pandas as pd
import cv2
import os

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}
def draw_connections(frame, keypoints, edges, confidence_threshold):
    # print(keypoints)
    for edge, color in edges.items():
        p1, p2 = edge
        x1, y1, c1 = keypoints[p1]
        x2, y2, c2 = keypoints[p2]
        if (float(c1) > confidence_threshold) and (float(c2) > confidence_threshold):
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)


def draw_landmark(frame,bboxs,keypoints):   
    for bbox in bboxs:
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)      
    for keypoint_person in keypoints:
        for keypoint in keypoint_person:
            cv2.circle(frame, (int(keypoint[0]), int(keypoint[1])), 5, (0, 0, 255), -1)
        if keypoint_person.size >0:
            draw_connections(frame,keypoint_person,EDGES,0.5)
    return frame


def read_all_videos(input_folder,output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # List all files in the input folder
    files = os.listdir(input_folder)

    # Filter out only the MP4 files
    mp4_files = [f for f in files if f.endswith('.mp4')]
    input_path=[]
    output_path=[]
    for mp4_file in mp4_files:
        # Generate input and output paths
        input_path.append(os.path.join(input_folder, mp4_file))
        output_path.append(os.path.join(output_folder, f"output_{mp4_file}"))

    return input_path,output_path
###### Use model in video
# Load a model
model = YOLO('yolov8x-pose.pt')  # load an official model

# read video
# Set the input and output folders
input_folder = "Input_video/"

    
# Read path of all MP4 files in the input folder
files = os.listdir(input_folder)
header_list=['l_shoulder','r_shoulder','l_elbow','r_elbow','l_wrist','r_wrist','l_hip','r_hip']
df=pd.DataFrame(columns=header_list)


for file in files:
    if file.endswith('.mp4'):
        file_path = os.path.join(input_folder, file)
        # read video
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Cannot open camera or file")
            exit()

        # Save output video
        output_video = f"Output_video_Yolo/{file}_output.mp4"

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
            # Make Detection
            pose_result =model(frame)
            # box around of all persons
            bboxs=pose_result[0].boxes.data.cpu().numpy().astype(int)
            #landmarks for all persons
            keypoints = pose_result[0].keypoints.data.cpu().numpy().astype(float)
            
            if len(keypoints)>0:
                frame=draw_landmark(frame,bboxs,keypoints)
                for keypoint in keypoints:
                    landmarks_interest=[[keypoint[5][0],keypoint[5][1]],[keypoint[6][0],keypoint[6][1]],[keypoint[7][0],keypoint[7][1]],[keypoint[8][0],keypoint[8][1]],[keypoint[9][0],keypoint[9][1]],
                                        [keypoint[10][0],keypoint[10][1]],[keypoint[11][0],keypoint[11][1]],[keypoint[12][0],keypoint[12][1]]]
                    df.loc[len(df)] = landmarks_interest
            cv2.imshow("Video",frame)
            video_writer.write(frame)
            if cv2.waitKey(1) == ord('q') or not ret:
                break
            df.to_csv(f"Yolo_CSV/{file}.csv",index = False)
# When everything done, release the capture
cap.release()
video_writer.release()
cv2.destroyAllWindows()

