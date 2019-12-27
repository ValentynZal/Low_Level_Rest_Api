from pymongo import MongoClient


# client = MongoClient("mongodb://localhost:27017/")
# db = client['database'] 
# users = db['users']
# install `mongodb`
# > `sudo service mongodb start`
# add path to mongo "connector" to the end of ~/.bashrc
# > `source ~/.bashrc`

client = MongoClient('mongodb+srv://valentyn:val11091994@cluster0-zl8k4.mongodb.net/test?retryWrites=true&w=majority') #  --username valentyn
db = client['database']
users = db['users'] # collection
# print(users, 'USERS HERER')


