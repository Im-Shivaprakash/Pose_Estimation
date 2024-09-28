import pymongo
import pandas as pd
from datetime import datetime

def connect_to_mongo(db_name, collection_name, uri="mongodb://localhost:27017/"):
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

def generate_unique_workout_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def structure_data_with_sets(df, workout_id):
    # Initialize the document structure
    workout_document = {
        "workout_id": workout_id,
        "date": datetime.now(),
        "sets": []
    }

    # Group by set number and create a nested structure for each set
    grouped_sets = df.groupby('Set Number')

    for set_no, group in grouped_sets:
        set_data = {
            "set_no": set_no,
            "exercises": []
        }
        # Loop through the group to add exercises and reps
        for _, row in group.iterrows():
            exercise_data = {
                "exercise_name": row["Exercise"],
                "reps": row["Reps"]
            }
            set_data["exercises"].append(exercise_data)

        # Add each set data to the workout document
        workout_document["sets"].append(set_data)

    return workout_document

def upload_to_mongo(workout_document, collection):
    # Insert the structured document into MongoDB
    collection.insert_one(workout_document)
    print("Data successfully uploaded to MongoDB.")

def main():
    # Read the workout data from CSV
    df = pd.read_csv("workout_data.csv")
    
    # Generate a unique workout ID
    workout_id = generate_unique_workout_id()
    print(f"Unique ID: {workout_id}")
    
    # Structure the data to include workout ID, sets, and exercises
    workout_document = structure_data_with_sets(df, workout_id)
    print(f"Structured Workout Data:\n{workout_document}")
    
    # Connect to MongoDB
    collection = connect_to_mongo("Workout_db", "exercise_data")
    
    # Upload structured document to MongoDB
    upload_to_mongo(workout_document, collection)

if __name__ == "__main__":
    main()
