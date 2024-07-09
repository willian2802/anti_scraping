import re
import hashlib
import platform
from collections import defaultdict
from flask import request
from datetime import datetime
# import tkinter as tk

# to use this i need to install screeninfo
# from screeninfo import get_monitors


# +--------------------------- lists ---------------------------

black_list_IP = ["192.168.0.44", "192.168.0.75"]
yellow_list_IP = []
green_list_IP = []

# Dicionário para armazenar a última requisição de cada IP, o fingerprint do IP e o limite
# limite = numero de vezes em que o IP pode fazer requisições em um curto perido de horário
# antes de ser bloquiado
last_request_time = {}
fingerprint_list = {}
request_limits = defaultdict(int)


# informaçoes individuais de usuario
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
        


# --------------------------- block bots ---------------------------

def block_user_for():

    # ------------------ informaçoes da requisição ------------------

    # pega o IP o user_agent o tempo do request etc...
    ip_address = request.remote_addr
    user_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    PATH = request.path
    user_agent = request.headers.get('User-Agent')
    sistema_operacional = platform.system()
    
    # uma descriçao para o log ou outras informaçoes uteis
    coment = "None"



    # ------------------ pega o tamanho da tela do usuario ------------------
    # monitors = get_monitors()
    # if monitors:
    #     tamanho_tela = (monitors[0].width, monitors[0].height)
    # else:
    #     tamanho_tela = (0, 0)


    # ------------------ pega o tamanho da tela do usario ------------------
    # # Cria uma instância da janela Tkinter
    # root = tk.Tk()

    # # Obtém a largura e altura da tela
    # largura_tela = root.winfo_screenwidth()
    # altura_tela = root.winfo_screenheight()

    # # Fecha a janela Tkinter
    # root.destroy()

    # # Armazena o tamanho da tela na variável
    # tamanho_tela = (largura_tela, altura_tela)


    # ------------------ Create finger-print ------------------
     
    # Combina os dois IPs em uma única string
    combined_data = f"{sistema_operacional}-{user_agent}"
    # Cria um objeto hash SHA-256
    hash_object = hashlib.sha256()
    # Atualiza o objeto hash com os dados combinados (codificados em bytes)
    hash_object.update(combined_data.encode('utf-8'))
    # Obtém o hash hexadecimal
    New_fingerprint = hash_object.hexdigest()

    # ------------------ block requests com muitas requisições em um curto período de tempo e verifica o fingerprint ------------------

    # Obtendo o tempo atual como objeto datetime
    # nao funciona pegando o user_time 
    tempo_atual = datetime.now()
    
    if ip_address not in last_request_time:
        last_request_time[ip_address] = tempo_atual.strftime('%Y-%m-%d %H:%M:%S')
        request_limits[ip_address] = 0
        fingerprint_list[ip_address] = New_fingerprint
    else:
        # se o fingerprint da ultima requisição for diferente do 
        # fingerprint que o usuario esta usando agora Blockeia o acesso e adiciona na yellow_list
        if fingerprint_list[ip_address] != New_fingerprint:
            coment = "Por favor so acesse o site com o dispositivo que voce acessou na primeira vez"
            yellow_list_IP.append(ip_address)
            # cria e adicina o log
            log = Request_Log(tempo_atual, ip_address, PATH, user_agent, New_fingerprint, coment)
            log.create_log()
            # O true indica que o acesso nao passou na verificaçao de segurança
            return (True,coment)

        # Convertendo last_request_time[ip_address] para objeto datetime
        last_request_time_ip = datetime.strptime(last_request_time[ip_address], '%Y-%m-%d %H:%M:%S')
        
        # Calculando a diferença de tempo em segundos
        time_difference = (tempo_atual - last_request_time_ip).total_seconds()
        
        # Atualizando last_request_time[ip_address] para o tempo atual
        last_request_time[ip_address] = tempo_atual.strftime('%Y-%m-%d %H:%M:%S')


    #Nota: no futuro modificar para o contador tambem usar o fingerprint nao so o IP bloquiar o acesso
        # Se a diferença de tempo for menor que 10 segundos
        if time_difference < 10:
            request_limits[ip_address] += 1

            # limite de vezes em que a requisiçao pode passar dos segundos minimos entre requisiçoes
            if request_limits[ip_address] > 5:
                coment = "bloqueado por enviar multiplos requests em um curto periodo de tempo"
                yellow_list_IP.append(ip_address)
                # cria e adicina o log
                log = Request_Log(tempo_atual, ip_address, PATH, user_agent, New_fingerprint, coment)
                log.create_log()
                # O true indica que o acesso nao passou na verificaçao de segurança
                return (True,coment)
        else:
            # Resetar o limite se a diferença de tempo for maior ou igual a 10 segundos
            request_limits[ip_address] = 0

    # ------------------ request limits Now => is 10 ------------------    

    # Se passar de um certo número de requests, bloqueia o acesso
    # Dicionario para armazenar o numero de requisições por IP
    ip_count = defaultdict(int)
    for log in Logs:
        
        ip = log['user_ip']
        ip_count[ip] += 1

    if ip_count[ip_address] > 10: # limite de requisiçoes por IP atualment => 10
        coment = "Chegou a quantidade maxima de requisições por IP"
        yellow_list_IP.append(ip_address)
        # cria e adicina o log
        log = Request_Log(tempo_atual, ip_address, PATH, user_agent, New_fingerprint, coment)
        log.create_log()
        # O true indica que o acesso nao passou na verificaçao de segurança
        return (True,coment)
        

    # ------------------ Agent blocker ------------------    
    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if re.search(r'\bbot\b', user_agent, re.IGNORECASE) or re.search(r'\bscraper\b', user_agent, re.IGNORECASE):
        coment = "bloquiado por usar bots ou por scraping"
        # cria e adicina o log
        log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
        log.create_log()
        return (True,coment)
    
    # se o agente for "headless" nao vai ter acesso ao site
    if re.search(r'\bheadless\b', user_agent, re.IGNORECASE):
        coment = "bloquiado por usar agente headless"
        # cria e adicina o log
        log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
        log.create_log()
        # O true indica que o acesso nao passou na verificaçao de segurança
        return (True,coment)
    

    # ------------------ verifica se o IP esta em uma das listas ------------------    

    # bloqueia os IPs que estiverem na black list ou na yellow list e adiciona um comentario
    if ip_address in black_list_IP or ip_address in yellow_list_IP:
        coment = "IP esta em uma das listas de bloqueio"

        # cria e adicina o log
        log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
        log.create_log()
        
        # O true indica que o acesso nao passou na verificaçao de segurança
        return (True,coment)

    # ------------------ no final de tudo ------------------    
     
    # se o acesso passou por todas as verificacoes, o acesso pode ser autorizado
    coment = "Acesso autorizado"

    # cria e adicina o log
    log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    log.create_log()
    # O false indica que o acesso passou na verificaçao de segurança
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


