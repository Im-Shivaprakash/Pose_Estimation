import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Define the exercise threshold and counter
threshold = 0.76  # Adjust based on your exercise
reps = 0
is_up = False

def count_burpee_reps(landmarks):
    global reps, is_up
    # Average y-coordinates of hips
    hip_y = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y + 
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y) / 2  
    
    # Check for the threshold condition to count reps
    if is_up and hip_y < threshold:
        reps += 1
        is_up = False
    elif not is_up and hip_y > threshold:
        is_up = True



def track_burpees():
    cap = cv2.VideoCapture(0)
    
    # vid_width = int(cap.get(3))
    # vid_height = int(cap.get(4))

    # out = cv2.VideoWriter('burpees.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, frameSize=(vid_width, vid_height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # out.write(frame)
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            count_burpee_reps(landmarks)
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(frame, f'Reps: {reps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Burpees Counter', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the burpee tracking
track_burpees()
