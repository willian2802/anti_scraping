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

def add_IP_data_to_DB(new_ip_data):

    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Selecionar uma coleção
    colecao = db['IP_Data']

    # insere o log no DB
    colecao.insert_one(new_ip_data)
    
    print (f"Document inserted with ID: {new_ip_data}")

    # fecha a conexação com o DB
    # client.close()

def get_ip_data_from_db(ip_address):
    
    db = client['sample_mflix']
    colecao = db['IP_Data']

    # Encontrar o documento que contém o IP especificado como uma chave no documento
    data = colecao.find_one({ip_address: {"$exists": True}})
    
    print(data)
    # Se encontrado, retorna os dados do IP específico
    if data and ip_address in data:
        return data[ip_address]
    return None

get_ip_data_from_db("127.0.0.1")
