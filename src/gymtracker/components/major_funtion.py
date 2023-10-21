import cv2
import mediapipe as mp
import numpy as np
mp_drawing= mp.solutions.drawing_utils
mp_pose= mp.solutions.pose 
import yaml
from gymtracker.utils.common import read_yaml, calculate_angle
from pathlib import Path
from gymtracker import logger

params= read_yaml(Path("params.yaml"))


class Track:

    def run_algo():
        cap= cv2.VideoCapture(0)   # here 0 is the default video capture [ here its webcam ], we can give 1 for secondary camera


        counter= 0
        stage= None


        with mp_pose.Pose(min_detection_confidence= params.min_detection_confidence, min_tracking_confidence= params.min_tracking_confidence) as pose:
            
            while cap.isOpened():
                ret, frame= cap.read()
                
                # Detect stuff and render
                image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Open cv reads the image as BGR, but mediapipe needs RGB
                image.flags.writeable= False                    # Now its read only, saving us some memory
                
                
                # Make detection
                results= pose.process(image)
                
                # Recolour back to BGR
                
                image.flags.writeable = True
                image= cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Extract landmarks
                try:
                    landmarks= results.pose_landmarks.landmark
                    
                    #Getting coordinates
                    shoulder= [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    elbow= [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    wrist= [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    angle= calculate_angle(shoulder, elbow, wrist)
                    
                    # Visualize angle
                    cv2.putText(image, str(angle),
                                tuple(np.multiply(elbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA   # size, color, linewidth, linetype
                            )
                    
                    # Curl counter logic

                    up_val= params.curl_up_threshold
                    downval= params.curl_down_threshold
                    
                    if angle < up_val:
                        stage= "up"
                    if angle > downval and stage=='up':
                        stage= 'down'
                        counter+= 1
                        print(counter)       
                    
                except Exception as e:
                    raise e
                    #pass
                
                # Render curl counder

                # setup status box
                rect_color= params.rectangle_color
                cv2.rectangle(image, (0,0), (225,73), rect_color, -1)  # input, start point, end point, colur, fill color or not
                
                # Rep data

                title_color= params.title_font_color
                value_color= params.rep_and_stage_color
                
                cv2.putText(image, "REPS", (7,15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, title_color, 1, cv2.LINE_AA
                        )
                
                cv2.putText(image, str(counter), (10,60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, value_color, 2, cv2.LINE_AA
                            )
                
                
                # stage data
                
                cv2.putText(image, "STAGE", (75,15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, title_color, 1, cv2.LINE_AA
                    )
                
                cv2.putText(image, str(stage), (80,60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, value_color, 2, cv2.LINE_AA
                            )
                
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(85,255,85), thickness=2, circle_radius=2), # landmark
                                        connection_drawing_spec= mp_drawing.DrawingSpec(color=(50,21,201), thickness=2))  # connections
                                        
                
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord(params.window_close_key):
                    logger.info(f"You succesfully completed {counter} reps of Bicep curls")
                    break


            cap.release()           # release the video capture
            cv2.destroyAllWindows()  # If q is clicked close the window