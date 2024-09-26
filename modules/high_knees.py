import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose

# Define thresholds for knee movement
knee_up_threshold = 0.1  # Threshold for knee to be considered "up"
knee_down_threshold = 0.1  # Threshold for knee to be considered "down"

reps = 0
left_knee_up = False
right_knee_up = False

def count_high_knees_reps(landmarks):
    global reps, left_knee_up, right_knee_up

    left_knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y
    right_knee_y = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y
    left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
    right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

    left_knee_relative_y = left_knee_y - left_hip_y
    right_knee_relative_y = right_knee_y - right_hip_y

    # Check left knee movement
    if left_knee_relative_y > knee_up_threshold and not left_knee_up:
        left_knee_up = True  # Mark knee as up
    elif left_knee_relative_y < -knee_down_threshold and left_knee_up:
        reps += 1  # Count as one full rep
        left_knee_up = False  # Reset for the next rep

    # Check right knee movement
    if right_knee_relative_y > knee_up_threshold and not right_knee_up:
        right_knee_up = True  # Mark knee as up
    elif right_knee_relative_y < -knee_down_threshold and right_knee_up:
        reps += 1  # Count as one full rep
        right_knee_up = False  # Reset for the next rep

    return reps
