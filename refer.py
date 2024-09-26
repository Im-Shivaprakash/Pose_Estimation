import cv2
import mediapipe as mp
import time
import pandas as pd 
from modules.burpees import count_burpee_reps as burpees
from modules.squats import count_squats as squats
from modules.high_knees import count_high_knees_reps as highknees
from modules.mountain_climbers import count_mountain_climber_reps as mountainclimbers

def workout_track(landmarks, current_workout):
    workout_list = {
        'burpees' : burpees,
        'squats' : squats,
        'high_knees' : highknees,
        'mountain_climbers' : mountainclimbers
    }
    
    if current_workout in workout_list:
        rep = workout_list[current_workout](landmarks)
        return rep

def main():
    
    try:
        preparation_time = int(input('Enter preparation time in seconds: '))
        workout_time = int(input('Enter workout time in seconds: '))
        rest_time = int(input('Enter rest time in seconds: '))
        num_sets = int(input('Enter number of sets: '))
    except ValueError:
        print("Invalid input. Please enter integer values.")
        return

    workout_cycles_per_set = []

    # Collect cycle data for the first set
    try:
        num_cycles = int(input(f'Enter number of cycles for set 1: '))
    except ValueError:
        print("Invalid input. Please enter an integer value.")
        return

    set_cycles = []
    for j in range(num_cycles):
        while True:
            workout_name = input(f'Enter workout name for cycle {j+1} of set 1 (high knees/burpees/mountain climbers/squats): ').strip().lower()
            if workout_name in ['high knees', 'burpees', 'mountain climbers', 'squats']:
                set_cycles.append(workout_name)
                break
            else:
                print("Invalid workout name. Please enter 'high knees', 'burpees', 'mountain climbers', or 'squats'.")
    workout_cycles_per_set.append(set_cycles)

    # Ask if sets should repeat
    if num_sets > 1:
        while True:
            repeat_sets = input('Do you want to repeat the data for all sets? (yes/no): ').strip().lower()
            if repeat_sets in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if repeat_sets == 'no':
            # Collect data for the remaining sets if not repeating
            for i in range(1, num_sets):
                try:
                    num_cycles = int(input(f'Enter number of cycles for set {i+1}: '))
                except ValueError:
                    print("Invalid input. Please enter an integer value.")
                    return
                set_cycles = []
                for j in range(num_cycles):
                    while True:
                        workout_name = input(f'Enter workout name for cycle {j+1} of set {i+1} (high knees/burpees/mountain climbers/squats): ').strip().lower()
                        if workout_name in ['high knees', 'burpees', 'mountain climbers', 'squats']:
                            set_cycles.append(workout_name)
                            break
                        else:
                            print("Invalid workout name. Please enter 'high knees', 'burpees', 'mountain climbers', or 'squats'.")
                workout_cycles_per_set.append(set_cycles)
        else:
            # Duplicate the data from the first set for all remaining sets
            workout_cycles_per_set.extend([workout_cycles_per_set[0]] * (num_sets - 1))

    # Debug: print workout cycle plan
    print("Workout plan for all sets:")
    for i, set_cycles in enumerate(workout_cycles_per_set):
        print(f"Set {i+1}: {set_cycles}")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot detect feed")
    exit()

# Initialize DataFrame to store reps data
columns = ['Set', 'Cycle', 'Exercise', 'Reps']
reps_data = pd.DataFrame(columns=columns)

# Placeholder for total reps and flags
prep_flag = False

# Track start time
start_time = time.time()

# Begin the tracking process
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_image)  # Assuming 'pose' is your Pose model from MediaPipe
    
    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark
        elapsed_time = time.time() - start_time
        
        # Preparation phase
        if elapsed_time < workout_data['preparation_time']:
            cv2.putText(frame, "Get Ready", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f"Time Left: {workout_data['preparation_time'] - int(elapsed_time)}s",
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            prep_flag = True

        # After preparation, begin workout
        if prep_flag:
            for set_data in workout_data['sets']:
                set_num = set_data['set_num']
                total_reps = 0
                
                for cycle_num, exercise_name in enumerate(set_data['cycles'], start=1):
                    start_time = time.time()
                    current_time = 0
                    current_reps = 0
                    
                    # Perform exercise for the set workout time
                    while current_time < workout_data['workout_time']:
                        current_reps += workout_track(landmarks, exercise_name)  # Your tracking logic
                        current_time = time.time() - start_time
                        cv2.putText(frame, f'Reps: {current_reps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    # Store reps data into DataFrame after each exercise
                    reps_data = pd.concat([reps_data, pd.DataFrame({
                        'Set': [set_num],
                        'Cycle': [cycle_num],
                        'Exercise': [exercise_name],
                        'Reps': [current_reps]
                    })], ignore_index=True)

                    
                    # Rest phase
                    start_rest_time = time.time()
                    rest_time = 0
                    while rest_time < workout_data['rest_time']:
                        rest_time = time.time() - start_rest_time
                        cv2.putText(frame, "Rest", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        cv2.putText(frame, f"Time Left: {workout_data['rest_time'] - int(rest_time)}s", 
                                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # Display the frame
    cv2.imshow('tracker', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Print or save the DataFrame with reps data
print(reps_data)
reps_data.to_csv('workout_reps_data.csv', index=False)




    # Initialize DataFrame to store reps data
    columns = ['Set', 'Cycle', 'Exercise', 'Reps']
    reps_data = pd.DataFrame(columns=columns)

    # Placeholder for total reps and flags
    prep_flag = False

    # Track start time
    start_time = time.time()

    # Begin the tracking process
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preparation phase
        elapsed_time = time.time() - start_time
        if elapsed_time < workout_data['preparation_time']:
            cv2.putText(frame, "Get Ready", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, f"Time Left: {workout_data['preparation_time'] - int(elapsed_time)}s",
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            prep_flag = True
        
        if prep_flag:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb_image)  # Assuming 'pose' is your Pose model from MediaPipe
            
            if result.pose_landmarks:
                landmarks = result.pose_landmarks.landmark
                

                # After preparation, begin workout
            