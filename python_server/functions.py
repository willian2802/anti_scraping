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

user_log_history = []


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

        

    if ip_count[ip_address] > 5: # limite de requisiçoes por IP
        yellow_list_IP.append(ip_address)

    print(user_log_history)


    limit = 0

    log_request_limitis_list = {
        'user_ip': ip_address,
        'time': user_time,
        "limit": limit 
    }
    user_log_history.append(log_request_limitis_list)

    time_diference = (user_time - log_request_limitis_list[ip_address]).total_seconds()
    last_request_time = user_time

    if time_diference > 5
        last_request_time["limit"] +=




    for ultimo_request in user_log_history:
        if (ultimo_request['time'] - (ultimo_request['time'] + 10) ).total_seconds() > 0:
            limit += 1
            print(limit)

    # print(user_log_history[ip_address])
    
    

    # for ultimo_request in user_log_history:
        # ip_count[cuu]

    #     if ultimos_request :

    

    #     if (user_time - user_log_history[ultimos_request]).total_seconds() > 10:
        


    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if "bot" in user_agent.lower() or "scraper" in user_agent.lower():
        coment = "bloquiado por causa do agente"
        return (True,coment)
    
    # se o agente for "headless" nao vai ter acesso ao site
    if "Headless" in user_agent:
        coment = "bloquiado por usar agente headless"
        return (True,coment)
    


    # ------------------ block requests com muitas requisições em um curto período de tempo ------------------

    # print(user_log_history[ip_address])

    # for ultimo_request in user_log_history:
        


    # if (user_time - user_log_history)

    # if (user_time - user_log_history[ip_address]).total_seconds() > 10:
    #         print("Muitas requisições em um curto período de tempo")
    #         coment = "Muitas requisições em um curto período de tempo"
    #         return (True,coment)
    
    user_log_history[ip_address] = user_time


    # cria e adicina o log
    log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    log.create_log()

    return (False,coment)



# modulos para adicionar

# Função para verificar atividade suspeita
def check_suspicious_activity(log):
    ip_address = log['user_ip']
    current_time = datetime.datetime.strptime(log['current_time'], "%Y-%m-%d %H:%M:%S")
    user_agent = log['user_agent']
    
    # Regras de atividade suspeita
    if 'scraper' in user_agent.lower() or 'bot' in user_agent.lower():
        ban_user(ip_address, "User agent suspeito")
        return True, "User agent suspeito"
    
    if ip_address in black_list_IP:
        return False, "IP já está na lista de bloqueio"
    
    if ip_address in yellow_list_IP:
        # Verifica se há muitas requisições em um curto período de tempo
        if (current_time - user_log_history[ip_address]).total_seconds() < 10:
            ban_user(ip_address, "Muitas requisições em um curto período de tempo")
            return True, "Muitas requisições em um curto período de tempo"

    
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


