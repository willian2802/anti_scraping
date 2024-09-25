# MONGODB_URI = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import UpdateOne

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
    

# ----------- Add DATA DB -----------

# def add_to_ConfigList(toAdd, listName):

#     # Selecionar o banco de dados
#     db = client['sample_mflix']

#     # Selecionar uma coleção
#     colecao = db['ConfigList']


#     colecao.update_one(
#         {"_id": listName},
#         {"$push": {"list": toAdd}}
#     )



def add_log_to_DB(log):

    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Selecionar uma coleção
    colecao = db['Logs']

    # insere o log no DB
    colecao.insert_one(log)
    

# ----------- IP DATA DB -----------

def delete_IP_data_from_DB(ip_address):
    db = client['sample_mflix']
    colecao = db['IP_Data']

    # apaga o documteto do DB
    colecao.delete_one({"_id": ip_address})


def add_IP_data_to_DB(ip_address, data):
    db = client['sample_mflix']
    colecao = db['IP_Data']

    update = {"$set": data}  # Update the existing document with the new data
    filter = {"_id": ip_address}  # Filter the document by _id

    # atualiza o IP_data no DB
    result = colecao.update_one(filter, update)

    # se nada for encontrado, insere um novo IP_data no DB
    if result.matched_count == 0:
        document = {"_id": ip_address, **data}
        colecao.insert_one(document)

# ------------  get DATA from DB -----------

def get_ip_data_from_db(ip_address):
    db = client['sample_mflix']
    colecao = db['IP_Data']

    # cria o dicionário vazio para receber os dados
    data = {}

    # acha o documento que contém o ip_address como _id
    result = colecao.find_one({"_id": ip_address})

    if result:
        data = result

    # If found, return the data of the specific IP
    if data:
        return data
    return False


def get_list_from_DB(list_name):
    db = client['sample_mflix']
    colecao = db['ConfigList']

    list = colecao.find_one({"_id": list_name})

    return list

# retorna True, estiver dentro da lista se nao retorna False
def check_if_is_in(to_check, list_name):

    print(to_check)
    print(list_name)

    db = client['sample_mflix']
    colecao = db['ConfigList']

    query = {"_id": list_name, "list": to_check}
    result = colecao.find_one(query)

    print("result: check_if_is_in" + str(result))    
    if result:
        return (True)
    else:
        return (False)




def insert_to_list(nome_da_lista, insert_value):
    db = client['sample_mflix']
    colecao = db['ConfigList']

    # Atualiza a lista com o novo valor
    colecao.update_one({"_id": nome_da_lista}, {"$addToSet": {"list": insert_value}})

