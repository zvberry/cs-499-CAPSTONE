from pymongo import MongoClient

class AnimalShelter(object):
    def __init__(self):
       USER = 'accuser'
       PASS = 'wm2360'
       HOST = 'localhost'
       PORT = 27017
       DB = 'AAC'
       COL = 'animals'

       self.client = MongoClient(f'mongodb://aacuser:wm2360@nv-desktop-services.apporto.com:31475')
       self.database = self.client[DB]
       self.collection = self.database[COL]

    def create(self, data):
        if data:
            try:
                result = self.collection.insert_one(data)
                return True if result.inserted_id else False
            except Exception as e:
                print(f"Insert Error: {e}")
                return False
        else:
             raise ValueError("Empty data cannot be inserted.")

    def read(self, quary):
        try:
            result = list(self.collection.find(quary))
            return result
        except Exception as e:
            print(f"Query Error: {e}")
            return []

    def update(self, quary, new_values):
        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.delete_count
        except Exception as e:
            print(f"Delete Error: {e}")
            return 0
    def delete(self, query):
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Delete Error: {e}")
            return 0
