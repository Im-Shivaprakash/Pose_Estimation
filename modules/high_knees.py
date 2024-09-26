# high_knees.py

import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

alignment_tolerance = 0.1  # Adjust as necessary
high_knee_in_progress = False  # Global variable for high knee state

def check_high_knee_conditions(landmarks):
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]

    hip_pos = np.array([hip.x, hip.y])
    knee_pos = np.array([knee.x, knee.y])

    knee_above_hip = knee_pos[1] > hip_pos[1]

    return knee_above_hip

def count_high_knees(landmarks):
    global high_knee_in_progress  # Keep track of high knee state globally

    knee_above_hip = check_high_knee_conditions(landmarks)

    # Detect when a high knee is in progress
    if not high_knee_in_progress and knee_above_hip:
        high_knee_in_progress = True  # High knee has started
        return 0  # No rep yet, just started the high knee
    
    # Detect when high knee is completed (knee back down)
    elif high_knee_in_progress and not knee_above_hip:
        high_knee_in_progress = False  # High knee completed, reset state
        return 1  # Count 1 rep

    return 0
