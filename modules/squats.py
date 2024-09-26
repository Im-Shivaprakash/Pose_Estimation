import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

alignment_tolerance = 0.1  # Adjust as necessary
squat_in_progress = False  # Global variable for squat state

def check_squat_conditions(landmarks):
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    foot_index = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

    hip_pos = np.array([hip.x, hip.y])
    knee_pos = np.array([knee.x, knee.y])
    angle = np.degrees(np.arctan2(knee_pos[1] - hip_pos[1], knee_pos[0] - hip_pos[0]))

    hips_back_angle = 35 <= angle <= 45
    knee_not_over_foot = knee.x < foot_index.x

    return hips_back_angle, knee_not_over_foot

def is_initial_standing(landmarks):
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

    return (abs(shoulder.x - hip.x) < alignment_tolerance and
            abs(hip.x - knee.x) < alignment_tolerance and
            abs(knee.x - ankle.x) < alignment_tolerance)

squat_in_progress = False  # Initialize the squat state

def count_squats(landmarks):
    global squat_in_progress  # Keep track of squat state globally

    standing_pose = is_initial_standing(landmarks)
    hips_back_angle, knee_not_over_foot = check_squat_conditions(landmarks)

    # Detect when a squat is in progress
    if not squat_in_progress and hips_back_angle and knee_not_over_foot:
        squat_in_progress = True  # Squat has started
        return 0  # No rep yet, just started the squat
    
    # Detect when squat is completed (returning to standing position)
    elif squat_in_progress and standing_pose:
        squat_in_progress = False  # Squat completed, reset state
        return 1  # Count 1 rep

    return 0