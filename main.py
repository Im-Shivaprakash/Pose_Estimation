import cv2
import mediapipe as mp
import time
import pandas as pd 
from modules.burpees import count_burpee_reps as burpees
from modules.squats import count_squats as squats
from modules.high_knees import count_high_knees as highknees
from modules.mountain_climbers import count_mountain_climber_reps as mountainclimbers
import subprocess

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def run_database_connection():
    result = subprocess.run(['python', 'database_connection.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("database_connection.py executed successfully.")
    else:
        print(f"Error running database_connection.py:\n{result.stderr}")


def main():
    # Placeholder for workout data
    workout_data = {}
    # Dictionary to track the reps count for each exercise type
    reps_dict = {}

    # Step 1: Get Preparation time, Workout time, and Rest time
    workout_data['preparation_time'] = int(input("Enter preparation time in seconds: "))
    workout_data['workout_time'] = int(input("Enter workout time in seconds: "))
    workout_data['rest_time'] = int(input("Enter rest time in seconds: "))

    # Step 2: Get the number of sets
    num_sets = int(input("Enter the number of sets: "))
    workout_data['sets'] = []

    # Step 3: Loop through each set to get workout details
    for set_num in range(1, num_sets + 1):
        set_data = {'set_num': set_num, 'cycles': []}

        # Step 4: Get the number of cycles for set 1
        if set_num == 1:
            num_cycles = int(input(f"Enter the number of cycles for set {set_num}: "))
        else:
            repeat_cycles = input("Do you want to repeat the cycle data from the previous set? (yes/no): ").lower()
            if repeat_cycles == 'yes':
                set_data['cycles'] = workout_data['sets'][0]['cycles']  # Copy from set 1
                workout_data['sets'].append(set_data)
                continue
            else:
                num_cycles = int(input(f"Enter the number of cycles for set {set_num}: "))

        # Step 5: Get exercises for each cycle in the set
        for cycle_num in range(1, num_cycles + 1):
            exercise_name = input(f"Enter workout name for cycle {cycle_num} of set {set_num}: ")
            set_data['cycles'].append(exercise_name)

            # Initialize rep tracking for each exercise cycle
            if exercise_name not in reps_dict:
                reps_dict[exercise_name] = 0  # Initialize the reps count for this exercise

        # Store the set data
        workout_data['sets'].append(set_data)
    
    # Initialize Pandas DataFrame to store workout data
    columns = ['Set Number', 'Exercise', 'Reps']
    workout_df = pd.DataFrame(columns=columns)

    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot detect feed")
        exit()

    flip_horizontal = True

    # Preparation time countdown
    if workout_data['preparation_time'] > 0:
        print(f'Starting preparation time: {workout_data["preparation_time"]} seconds')
        start_prep_time = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read from camera")
                break
            
            elapsed_prep = time.time() - start_prep_time
            time_left = int(workout_data['preparation_time'] - elapsed_prep)
            if time_left < 0:
                break
            
            if flip_horizontal:
                frame = cv2.flip(frame, 1)
            
            cv2.putText(frame, 'Get Ready!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3, cv2.LINE_AA)
            cv2.putText(frame, f'Time Left: {time_left}s', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Workout Tracker', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return            
        print('Preparation time complete')
        







    for set_num in range(1, num_sets + 1):
        workout_cycles = workout_data['sets'][set_num - 1]['cycles']

        for cycle_num, workout_name in enumerate(workout_cycles, start=1):
            print(f'Starting {workout_name} for set {set_num}, cycle {cycle_num}')

            # Initialize reps to 0 for each cycle
            start_time = time.time()
            end_time = start_time + workout_data['workout_time']
            rep_counter = 0

            while time.time() < end_time:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read from camera")
                    break

                if flip_horizontal:
                    frame = cv2.flip(frame, 1)

                # Process pose landmarks
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    # Update reps based on workout type
                    if workout_name == 'burpees':
                        rep_counter += burpees(landmarks)
                    elif workout_name == 'squats':
                        rep_counter += squats(landmarks)
                    elif workout_name == 'high_knees':
                        rep_counter += highknees(landmarks)
                    elif workout_name == 'mountain_climbers':
                        rep_counter += mountainclimbers(landmarks)

                remaining_time = end_time - time.time()  # Correctly calculating remaining time
                if remaining_time < 0:
                    remaining_time = 0  # Prevent negative values

                minutes, seconds = divmod(int(remaining_time), 60)
                timer_display = f"{minutes:02}:{seconds:02}"

                # Drawing pose landmarks on the frame
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )

                # Overlay text for workout name, reps, and time left
                cv2.putText(frame, f'Workout: {workout_name.title()}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'Reps: {rep_counter}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'Time Left: {timer_display}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Use timer_display here

                # Show the frame
                cv2.imshow('Workout Tracker', frame)

                # Quit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return


            # After completing a cycle, update DataFrame with final reps count for this cycle
            reps_dict[workout_name] += rep_counter  # Keep track of reps over cycles
            new_row = {'Set Number': set_num, 'Exercise': workout_name, 'Reps': rep_counter}
            workout_df = pd.concat([workout_df, pd.DataFrame([new_row])], ignore_index=True)

            # Print cycle completion and reps
            print(f'Completed {workout_name} for set {set_num}, cycle {cycle_num}, reps: {rep_counter}')

            # Display updated workout DataFrame after every cycle
            print('\nWorkout Data:')
            print(workout_df)

            # Reset reps for the next cycle
            rep_counter = 0






            # Start rest period
            print(f'Rest for {workout_data["rest_time"]} seconds.')
            rest_start_time = time.time()
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read from camera.")
                    break

                if flip_horizontal:
                    frame = cv2.flip(frame, 1)

                elapsed_rest = time.time() - rest_start_time
                time_left = int(workout_data['rest_time'] - elapsed_rest)
                if time_left < 0:
                    break

                cv2.putText(frame, 'Resting...', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3, cv2.LINE_AA)
                cv2.putText(frame, f'Time Left: {time_left}s', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Workout Tracker', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            print(f'Rest time complete.')
        
    print('Workout complete.')
    cap.release()
    cv2.destroyAllWindows()

    # Save the workout data to a CSV file
    workout_df.to_csv('workout_data.csv', index=False)
    print('Workout data saved to workout_data.csv')
    
    run_database_connection()

if __name__ == '__main__':
    main()
