# MONGODB_URI = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


def connect_to_mongo():
    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return "You successfully connected to MongoDB!"
    except Exception as e:
        print(e)
        return "Failed to connect to MongoDB"

def add_log_to_DB(log):

    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Selecionar uma coleção
    colecao = db['Logs']

    # insere o log no DB
    colecao.insert_one(log)
    
    print (f"Document inserted with ID: {log}")

    # fecha a conexação com o DB
    # client.close()

# ----------- IP DATA DB -----------

def add_IP_data_to_DB(ip_address, data):
    db = client['sample_mflix']
    colecao = db['IP_Data']

    # Create a document with the ip_address as the _id
    document = {"_id": ip_address, **data}

    # Insert the document into the collection
    colecao.insert_one(document)

    print("IP_DATA_DB: is on!!!")
    print(f"Document inserted with ID: {ip_address}")
    # fecha a conexação com o DB
    # client.close()

# documents = collection.find({})
# for doc in documents:
#     for ip, data in doc.items():
#         if ip != "_id":
#             new_doc = data
#             new_doc["_id"] = ip
#             collection.insert_one(new_doc)
#     collection.delete_one({"_id": doc["_id"]})

# print("Estrutura reorganizada com sucesso!")


def get_ip_data_from_db(ip_address):
    db = client['sample_mflix']
    colecao = db['IP_Data']

    # Define the data variable
    data = {}

    # Find the document that contains the specified IP address as a key in the document
    result = colecao.find_one({"_id": ip_address})

    if result:
        data = result

    print(data)
    # If found, return the data of the specific IP
    if data:
        return data
    return False

