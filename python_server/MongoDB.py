# MONGODB_URI = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functions import Logs

uri = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def connect_to_mongo():

    # Selecionar o banco de dados
    db = client['nome_do_banco']

    # Selecionar uma coleção
    colecao = db['nome_da_colecao']

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return "You successfully connected to MongoDB!"
    except Exception as e:
        print(e)


def add_log_to_DB(log):
    colecao = db['logs']

    New_log = {
        'user_time': log.user_time,
        'ip_address': log.ip_address,
        'PATH': log.PATH,
        'user_agent': log.user_agent,
        'user_fingerprint': log.user_fingerprint,
        'coment': log.coment
    }
    colecao.insert_one(New_log)

    db = connect_to_mongo()

    # fecha a conexação com o DB
    client.close()
    # if db:
    #     log_request(db, "192.168.0.1", "abc123", "/home", "Mozilla/5.0", "Acesso autorizado")


