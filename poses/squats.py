import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Setup for video capture (use webcam)
cap = cv2.VideoCapture(0)

# Initialize a counter for repetitions
rep_counter = 0
squat_in_progress = False

# Set a threshold for alignment tolerance
alignment_tolerance = 0.1  # Adjust as necessary

def check_squat_conditions(landmarks):
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    foot_index = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

    # Vector calculations
    hip_pos = np.array([hip.x, hip.y])
    knee_pos = np.array([knee.x, knee.y])

    # Calculate angle using vector
    hip_to_knee = knee_pos - hip_pos

    # Angle calculations
    angle = np.degrees(np.arctan2(hip_to_knee[1], hip_to_knee[0]))

    # Conditions for squat
    hips_back_angle = 35 <= angle <= 45
    knee_not_over_foot = knee.x < foot_index.x

    return hips_back_angle, knee_not_over_foot

def is_initial_standing(landmarks):
    shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

    # Check if the landmarks are within the alignment tolerance
    return (abs(shoulder.x - hip.x) < alignment_tolerance and
            abs(hip.x - knee.x) < alignment_tolerance and
            abs(knee.x - ankle.x) < alignment_tolerance)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Check if in initial standing position
        standing_pose = is_initial_standing(landmarks)

        # Check conditions for squat
        hips_back_angle, knee_not_over_foot = check_squat_conditions(landmarks)

        # Detect squat progress
        if not standing_pose and hips_back_angle and knee_not_over_foot:
            squat_in_progress = True  # We are in the squat position
        elif standing_pose and squat_in_progress:
            # We completed a squat cycle
            rep_counter += 1
            squat_in_progress = False  # Reset the squat progress

        # Display the rep count
        cv2.putText(frame, f'Reps: {rep_counter}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # Draw landmarks
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('Squat Tracker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
