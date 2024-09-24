import cv2
import mediapipe as mp 

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils 

knee_up_threshold = 0.05
knee_down_threshold = 0.05
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
    
    if abs(left_knee_relative_y) <= knee_up_threshold:
        left_knee_up = True
    elif left_knee_relative_y > knee_down_threshold and left_knee_up:
        reps += 0.5
        left_knee_up = False

    if abs(right_knee_relative_y) <= knee_up_threshold:
        right_knee_up = True
    elif right_knee_relative_y > knee_down_threshold and right_knee_up:
        reps += 0.5
        right_knee_up = False

def track_high_knees():
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret , frame = cap.read()
        if not ret:
            break
    
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            count_high_knees_reps(landmarks)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        cv2.putText(frame, f'Reps: {int(reps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('High Knees Counter', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the mountain climber tracking
track_high_knees()
    
    
