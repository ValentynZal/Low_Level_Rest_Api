from pymongo import MongoClient
import dns


# client = MongoClient("mongodb://localhost:27017/")
# db = client['database'] 
# users = db['users']


cluster = MongoClient('mongodb+srv://valentyn:val11091994@cluster0-zl8k4.mongodb.net/test?retryWrites=true&w=majority') #  --username valentyn
db = cluster['database']
users = db['users'] # collection



