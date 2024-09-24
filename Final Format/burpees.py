import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose

# Define the exercise threshold and counter
threshold = 0.76  # Adjust based on your exercise
is_up = False

def count_burpee_reps(landmarks):
    global is_up
    reps_increment = 0
    # Average y-coordinates of hips
    hip_y = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y + 
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y) / 2  
    
    # Check for the threshold condition to count reps
    if is_up and hip_y < threshold:
        reps_increment = 1  # Increment the rep when conditions are met
        is_up = False
    elif not is_up and hip_y > threshold:
        is_up = True

    return reps_increment  # Return 1 if rep is completed, 0 otherwise
