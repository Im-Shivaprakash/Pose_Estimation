import pymongo
import pandas as pd 

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['sample_db']
collection = db['workouts']

data = {
    "set" : [1,1,2,2],
    "workout" : ["Squats", "HighKnees", "Squats", "HighKnees"],
    "reps" : [5,10,5,10]
}

df = pd.DataFrame(data)

data_dict = df.to_dict(orient = "records")
collection.insert_many(data_dict)

for doc in collection.find():
    print(doc)

