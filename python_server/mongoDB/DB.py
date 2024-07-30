# import os
# import certifi
# from pymongo import MongoClient
# from dotenv import load_dotenv

# # Carregar variáveis de ambiente do arquivo .env
# load_dotenv()

# # Obter a URI do MongoDB do arquivo .env
# MONGODB_URI = os.getenv('MONGODB_URI')

# # Caminho para o certificado SSL
# ca = certifi.where()

# # Conectar ao MongoDB usando a URI e o certificado SSL
# client = MongoClient(MONGODB_URI, tlsCAFile=ca)

# # Listar nomes dos bancos de dados para verificar a conexão
# try:
#     for db in client.list_database_names():
#         print(db)
# except Exception as e:
#     print(f"Erro ao listar bancos de dados: {e}")


# ------------------------------ test ------------------------------



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Selecionar o banco de dados
db = client['nome_do_banco']

# Selecionar uma coleção
colecao = db['nome_da_colecao']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
