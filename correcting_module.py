import cv2
import time
from modules.squats import count_squats
from edit_high_knees import count_high_knees  # Import the high knees counting function
import mediapipe as mp 

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def track_exercise_with_timer(workout_time, exercise_type):
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    end_time = start_time + workout_time
    rep_counter = 0  # Initialize rep counter for the specific exercise

    while time.time() < end_time:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Count reps based on the exercise type
            if exercise_type == 'squats':
                rep_counter += count_squats(landmarks)
            elif exercise_type == 'high_knees':
                rep_counter += count_high_knees(landmarks)

        # Display timer
        remaining_time = end_time - time.time()
        minutes, seconds = divmod(int(remaining_time), 60)
        timer_display = f"{minutes:02}:{seconds:02}"

        cv2.putText(frame, f'Time: {timer_display}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(frame, f'Reps: {rep_counter}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow(f'{exercise_type.capitalize()} Tracker', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Total {exercise_type} completed: {rep_counter}")
    return rep_counter

if __name__ == "__main__":
    workout_time = int(input("Enter the workout time in seconds: "))
    exercise_type = input("Enter the exercise type (squats/high_knees): ").strip().lower()
    
    if exercise_type not in ['squats', 'high_knees']:
        print("Invalid exercise type. Please enter 'squats' or 'high_knees'.")
    else:
        print(f"Starting {exercise_type} tracking...")
        track_exercise_with_timer(workout_time, exercise_type)
