import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose

# Define thresholds for knee movement
knee_in_threshold = 0.05
knee_out_threshold = 0.05

# Initialize global variables
reps = 0
left_knee_in = False
right_knee_in = False

def count_mountain_climber_reps(landmarks):
    global reps, left_knee_in, right_knee_in

    left_knee_x = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x
    right_knee_x = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x
    left_hip_x = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x
    right_hip_x = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x

    left_knee_relative_x = left_knee_x - left_hip_x
    right_knee_relative_x = right_knee_x - right_hip_x

    # Check left knee movement
    if left_knee_relative_x < -knee_in_threshold:  # Knee moving in
        left_knee_in = True
    elif left_knee_relative_x > knee_out_threshold and left_knee_in:  # Knee moving out
        reps += 1  # Count as one full rep
        left_knee_in = False  # Reset for the next rep

    # Check right knee movement
    if right_knee_relative_x < -knee_in_threshold:  # Knee moving in
        right_knee_in = True
    elif right_knee_relative_x > knee_out_threshold and right_knee_in:  # Knee moving out
        reps += 1  # Count as one full rep
        right_knee_in = False  # Reset for the next rep

    return reps
