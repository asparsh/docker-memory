from pymongo import MongoClient
from disney_memory_prediction.arima_model import arima_model

class connect_mongo():
    def __init__(self):
        time_model = arima_model()
        self.predictions = time_model.getPredictions()

    def insert(self):
        client = MongoClient('localhost', 27017)
        mydb = client.disney_database
        inserted_id = mydb.predictions.insert(self.predictions)



c = connect_mongo()
c.insert()