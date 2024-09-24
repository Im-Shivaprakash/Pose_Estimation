import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Define the thresholds for knee movement and the counter
knee_in_threshold = 0.05  # Adjust this based on the range of motion for the knee moving closer
knee_out_threshold = 0.05  # Adjust based on the knee moving back to starting position
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
    
    # Left knee movement
    if left_knee_relative_x < -knee_in_threshold:
        left_knee_in = True
    elif left_knee_relative_x > knee_out_threshold and left_knee_in:
        reps += 0.5
        left_knee_in = False

    # Right knee movement
    if right_knee_relative_x < -knee_in_threshold:
        right_knee_in = True
    elif right_knee_relative_x > knee_out_threshold and right_knee_in:
        reps += 0.5
        right_knee_in = False

def track_mountain_climbers():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            count_mountain_climber_reps(landmarks)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(frame, f'Reps: {int(reps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Mountain Climber Counter', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the mountain climber tracking
track_mountain_climbers()
