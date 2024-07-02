import hashlib
import platform
from collections import defaultdict
from flask import Flask, request, abort
from datetime import datetime, timedelta
import tkinter as tk


# +--------------------------- lists ---------------------------

black_list_IP = ["192.168.0.1", "192.168.0.2"]
yellow_list_IP = []
green_list_IP = []

# def remove_duplicates(black_list_IP, yellow_list_IP, green_list_IP):

#     black_list_IP = list(set(black_list_IP))
#     yellow_list_IP = list(set(yellow_list_IP))
#     green_list_IP = list(set(green_list_IP))

#     black_list_IP = remove_duplicates(black_list_IP)
#     yellow_list_IP = remove_duplicates(yellow_list_IP)
#     green_list_IP = remove_duplicates(green_list_IP)

#     return list(set(black_list_IP + yellow_list_IP + green_list_IP))


access_log = {}  #dicionário para registrar as requisições

User_information = []
Logs = [{
    'current_time': '00:00:00',
    'user_ip': '127.0.0.1',
    'user_agent': 'Mozilla/5.0',
    'path': '/views/index.html',
    'fingerprint': '1234567890'
}]
# --------------------------- Log Class ---------------------------
class Request_Log:
    def __init__(self, current_time, ip_address, path, agent, fingerprint,coment):
        self.current_time = current_time
        self.ip_address = ip_address
        self.path = path
        self.agent = agent
        self.fingerprint = fingerprint
        self.coment = coment

    def create_log(self):

        # generate a log
        log = {
        'current_time': self.current_time,
        'user_ip': self.ip_address,
        'user_agent': self.agent,
        'path': self.path,
        'fingerprint': self.fingerprint,
        'coment': self.coment
        }
        Logs.append(log)

    def show_log(self):
        return f"Current Time: {self.current_time}, IP: {self.ip_address}, Path: {self.path}, Agent: {self.agent}, Hash Code: {self.fingerprint}, Coment: {self.coment}"
    
    def show_all(self):
        return (Logs)


    # def remove(self):
    #     access_log[self.ip_address].remove(self.path)
        

# --------------------------- fingerprint ---------------------------



    # log = Request_Log(user_time, user_Ip, request.path, user_agent, fingerprint)
    # log.create_log()

    # return(Logs)

# --------------------------- block bots ---------------------------

def block_user_for():

    # pega o IP o  user_agent a o tempo do request etc...
    ip_address = request.remote_addr
    user_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    PATH = request.path
    user_agent = request.headers.get('User-Agent')
    sistema_operacional = platform.system()
    
    # uma descriçao para o log ou outras informaçoes uteis
    coment = "None"


    # ------------------ pega o tamanho da tela do usario ------------------
    # Cria uma instância da janela Tkinter
    root = tk.Tk()

    # Obtém a largura e altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Fecha a janela Tkinter
    root.destroy()

    # Armazena o tamanho da tela na variável
    tamanho_tela = (largura_tela, altura_tela)


    # ------------------ Create finger-print ------------------
     
    # Combina os dois IPs em uma única string
    combined_data = f"{tamanho_tela}-{sistema_operacional}-{user_agent}"
    # Cria um objeto hash SHA-256
    hash_object = hashlib.sha256()
    # Atualiza o objeto hash com os dados combinados (codificados em bytes)
    hash_object.update(combined_data.encode('utf-8'))
    # Obtém o hash hexadecimal
    New_fingerprint = hash_object.hexdigest()


    # Add the user's IP address to the list yellow_list_IP
    # if the request is more than a certain number of times

    # bloqueia os IPs que estiverem na black list ou na yellow list e adiciona um comentario
    if ip_address in black_list_IP or ip_address in yellow_list_IP:
        coment = "IP esta em uma das listas de bloqueio" 
        return (True,coment)

    # ------------------ request limits Now => is 5 ------------------
    # Se não estiver em nenhuma lista, calcula a quantidade de requests 
    # Se passar de um certo número de requests, bloqueia o acesso

    # Dictionary to store the count of each IP address in the logs
    ip_count = defaultdict(int)
    for log in Logs:

        ip = log['user_ip']
        ip_count[ip] += 1
        print(ip_count)

    if ip_address in ip_count and ip_count[ip_address] > 5:
        yellow_list_IP.append(ip_address)


    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if "bot" in user_agent.lower() or "scraper" in user_agent.lower():
        coment = "bloquiado por causa do agente"
        return (True,coment)
    
    # se o agente for "headless" nao vai ter acesso ao site
    if "Headless" in user_agent:
        coment = "bloquiado por usar agente headless"
        return (True,coment)
    

    # for log in Logs:
    #     if log['user_ip'] == ip_address:
    #        return (True,coment)

    # cria e adicina o log
    log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    log.create_log()

    return (False,coment)


    
# -------------------------------- update_access_log and list_IPs--------------------------------
# def add_IP_list():
#     user_ip = request.remote_addr
    


#     user_info = {
#             'user_ip': ip_address
#         }

#     # verifica se ja tem as informaçoes do usario
#     # se nao adiciona as informaçoes no user_info
#     if user_info not in User_information:
#         User_information.append(user_info)
    
#     # generate a log
#     log = {
#         'user_ip': user_ip,
#         'user_agent': user_agent,
#     }
#     Logs.append(log)
    

#     return f"user_ip: {user_ip}, user_agent: {user_agent}, logs list: {Logs}"



# def list_IPs_updated():
#     user_ip = request.remote_addr
#     user_agent = request.headers.get('User-Agent')

#     user_info = {
#             'user_ip': "121.121.121.121",
#             'user_agent': user_agent,
#         }

#     # verifica se ja tem as informaçoes do usario
#     # se nao adiciona as informaçoes no user_info
#     if user_info not in User_information:
#         logs.append(user_info)
    
#     # generate a log
#     log = {
#         'user_ip': user_ip,
#         'user_agent': user_agent,
#     }
#     logs.append(log)
    

#     return f"user_ip: {user_ip}, user_agent: {user_agent}, logs list: {logs}"


















    # ip_address = request.remote_addr
    # if ip_address not in access_log:
    #     access_log[ip_address] = []



    # # tempo_para_limpar = datetime.now() - timedelta(hours=6)

    # # for ip_user in access_log: 
    # #     if ip_user.current_time > tempo_para_limpar:
    # #         access_log[ip_address].remove("/endereco-de-processamento")
    # #         access_log[ip_address].remove("12:14:14")

    # # access_log[ip_address].append("/endereco-de-processamento")
    # # access_log[ip_address].append("12:14:14")
    # # access_log[ip_address].append("11:14:14")


    # return f"Access Log: {Logs}"

# -------------------------------- honneypot --------------------------------
def trap_activated():
    ip_address = request.remote_addr

    # pega o tempo do request
    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')

    #adiciona o ip na yellow list
    yellow_list_IP.append(request.remote_addr)


    if ip_address not in access_log:
        access_log[ip_address] = []
    
    # adiciona no access_log o path da requisição e o tempo da requisição
    access_log[ip_address].append(request.path)
    access_log[ip_address].append(current_time)

    return f"{access_log}"