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

def add_workout_id_to_df(df, workout_id):
    df["Workout_ID"] = workout_id
    return df

def upload_to_mongo(df, collection):
    data_dict = df.to_dict(orient="records")
    collection.insert_many(data_dict)
    print("Data successfully uploaded to MongoDB.")

def main():
    df = pd.read_csv("workout_data.csv")
    workout_id = generate_unique_workout_id()
    print(f"Unique ID: {workout_id}")
    
    df = add_workout_id_to_df(df, workout_id)
    print(f"Updated DataFrame with Workout ID:\n{df}")
    
    collection = connect_to_mongo("Workout_db", "exercise_data")
    
    upload_to_mongo(df, collection)

if __name__ == "__main__":
    main()
