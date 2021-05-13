from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('mongodb://localhost:27017/')
db=client.admin
# # Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

for x in range(1, 3):
    data = {
        'name' : 'hay',
        'rating' : 30
    }
    #Step 3: Insert data object directly into MongoDB via isnert_one
    result=db.reviews.insert_one(data)
    #Step 4: Print to the console the ObjectID of the new document
    print('Created {0} of 2 as {1}'.format(x,result.inserted_id))
#Step 5: Tell us that you are done
print('finished creating data reviews')