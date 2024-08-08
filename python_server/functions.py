import hashlib, platform, os, re
from collections import defaultdict
from flask import request, session, redirect, url_for
from datetime import datetime
from functools import wraps

# MongoDB
from MongoDB import add_log_to_DB, add_IP_data_to_DB, get_ip_data_from_db


# geolication
import requests
import json


# import tkinter as tk

# to use this i need to install screeninfo and geopy
# from screeninfo import get_monitors

# +--------------------------- lists ---------------------------

black_list_IP = ["192.168.0.44", "192.168.0.75"]
yellow_list_IP = []
green_list_IP = []

contry_black_list = ["China","India","Brazil","Russia"]


# dicionário para armazenar os IPs e seus atributos
DB_IP_Data = {}

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

        # cria e adiciona o log no DB
        log = {
        'current_time': self.current_time,
        'user_ip': self.ip_address,
        'user_agent': self.agent,
        'path': self.path,
        'fingerprint': self.fingerprint,
        'coment': self.coment
        }
        add_log_to_DB(log)

    def show_log(self):
        return f"Current Time: {self.current_time}, IP: {self.ip_address}, Path: {self.path}, Agent: {self.agent}, Hash Code: {self.fingerprint}, Coment: {self.coment}"
    
    def show_all(self):
        return (Logs)

# ------------------------------ verifica se e uma VPN ou uma proxy --------------------------------
# usando a API do IPQualityScore

# def is_anonymous_ip(ip_address):
#     api_key = "YOUR_API_KEY"  # Substitua pela sua chave de API do IPQualityScore
#     url = f"https://ipqualityscore.com/api/json/ip/{api_key}/{ip_address}"

#     response = requests.get(url)
#     data = response.json()

#     if data['proxy'] or data['vpn']:
#         return True
#     return False



# ------------------------------ Geolocalização --------------------------------

def get_ip_location(ip):
    ip_to_locate = ip

    # pega o nome do pais
    response = requests.get('http://ip-api.com/json/' + ip_to_locate + '?fields=country').json()
    return(response)

# ip = '127.0.0.1'

# def get_ip_location(ip):
#     ip_to_locate = ip
#     request_url = 'https://geolocation-db.com/jsonp/' + ip_to_locate


#     response = requests.get(request_url)

#     result = response.content.decode()
#     result = result.split("(")[1].strip(")")
#     result = json.loads(result)

#     # pega o nome do pais
#     country_name = result.get('country_name')
#     return country_name

# The_location = get_ip_location('198.6.3.18')
# print(The_location)

# ------------------------------ autenticação --------------------------------

# Função de verificação de autenticação

#verifica se a chave 'authenticated' está presente no dicionário session. 
# Se estiver presente, significa que o usuário está autenticado. 
# A sessão é um dicionário que o Flask usa para armazenar dados entre requisições.
def is_authenticated():
    return 'authenticated' in session


# um decoder usando isso adicionamos funçoes a mais em uma funçao ja existente
def login_required(f):
    print("login required is on!!!")

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            print("login required not authenticated!!!")
            return redirect(url_for('views.render_index'))
        return f(*args, **kwargs)
    return decorated_function

# --------------------------- block bots ---------------------------


# se retornar False significa que o acesso foi bloqueado
# se retornar True significa que o acesso foi liberado
def Securety_check():

    # ------------------ informaçoes da requisição ------------------

    # pega o IP o user_agent o tempo do request etc...
    ip_address = request.remote_addr
    user_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    PATH = request.path
    user_agent = request.headers.get('User-Agent')

    # # ------------------ informaçoes de localidade ------------------
    # country = get_ip_location(ip_address)
    # print(f"Country: {country}, City: {city}")
    
    # uma descriçao para o log ou outras informaçoes uteis
    coment = "None"



    # ------------------ pega o tamanho da tela do usuario ------------------
    # monitors = get_monitors()
    # if monitors:
    #     tamanho_tela = (monitors[0].width, monitors[0].height)
    # else:
    #     tamanho_tela = (0, 0)

    # ------------------ Create finger-print ------------------
    # Informações da CPU
    cpu_info = platform.processor()
    # Versão do SO
    sistema_operacional = platform.system()
    # Idioma do Sistema
    idioma_sistema = os.getenv('LANG', 'Unknown')
     


    # Combina os dois IPs em uma única string
    combined_data = f"{idioma_sistema}-{cpu_info}-{sistema_operacional}"
    # Cria um objeto hash SHA-256
    hash_object = hashlib.sha256()
    # Atualiza o objeto hash com os dados combinados (codificados em bytes)
    hash_object.update(combined_data.encode('utf-8'))
    # Obtém o hash hexadecimal
    New_fingerprint = hash_object.hexdigest()

    # ------------------ block Anonymous IP ------------------
    # if is_anonymous_ip(ip_address):
    #     coment = "Bloqueado por usar IP anônimo"
    #     log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    #     log.create_log()
    #     return (False, coment)


    # ------------------ block Location ------------------    
    # bloquei o acesso de acordo com as informações de localidade
    
    # if location[ip_address] in contry_black_list:
    #     coment = "Acesso não autorizado ao pais em que voce esta localizado"
    #     # cria e adicina o log
    #     log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    #     log.create_log()
    #     return (False,coment)

    # ------------------ block requests com muitas requisições em um curto período de tempo e verifica o fingerprint ------------------

    # Obtendo o tempo atual como objeto datetime
    # nao funciona pegando o user_time 
    tempo_atual = datetime.now()

    # ----------------- adiciona o IP_data no mongoDB -----------------


    # Buscar no DB o IP se tiver retorna o objeto se nao retorna False
    ip_data = get_ip_data_from_db(ip_address)
    # se o IP nao estiver no DB cria um novo ip_data para o novo IP
    if ip_data is False:

        # pega o pais do IP
        ip_location = get_ip_location(ip_address)

        # Adicionando um novo IP no dicionário
        new_ip_data = {
            "IP": ip_address,
            "suspicion_Level": 0,
            'Country': ip_location,
            "fingerprint": New_fingerprint,
            "request_count": 0,
            "request_time_limit_count": 0,
            "last_request_time": tempo_atual.strftime('%Y-%m-%d %H:%M:%S'),
            "time_to_delete": 24,
            "slow_down": "off",
            "slow_down_count": 0
        }
        # quando o IP entra no dicionário o tempo de acesso do IP e 12:00
        # assim evitando erro com o "slow_down" mode

        # adiciona o IP_data no mongoDB, o ip_address vai ser o "_id" do objeto no DB
        add_IP_data_to_DB(ip_address, new_ip_data)

        # pega o IP_data no mongoDB usando o IP
        ip_data = get_ip_data_from_db(ip_address)
        ip_data["last_request_time"] = tempo_atual.replace(hour=12, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')


    else:
        # pega o IP_data no mongoDB usando o IP
        ip_data = get_ip_data_from_db(ip_address)
        print("Esta funcionando")
        print(ip_data["Country"])

        # ------------ block by finger print ------------

        # se o fingerprint da ultima requisição for diferente do 
        # fingerprint que o usuario esta usando agora Blockeia o acesso e adiciona na yellow_list
        if ip_data["fingerprint"] != New_fingerprint:

            # aumenta o nivel de suspeita e adiciona um coment
            ip_data["suspicion_Level"] += 3
            coment += "Fingerptint: Alert, "
            

        # Convertendo last_request_time_ip para objeto datetime
        last_request_time_ip = datetime.strptime(ip_data["last_request_time"], '%Y-%m-%d %H:%M:%S')
        
        # Calculando a diferença de tempo em segundos
        time_difference = (tempo_atual - last_request_time_ip).total_seconds()
        
        # # Atualizando last_request_time[ip_address] para o tempo atual
        # last_request_time[ip_address] = tempo_atual.strftime('%Y-%m-%d %H:%M:%S')
        
        # ------------------- modo slow_down -------------------
        # limita a quantidade de requisições que pode ser feitas em um curto periodo de tempo
        # mas o acesso e liberado depois do tempo_minimo
        tempo_minimo = 60

        if ip_data["slow_down"] == "on":
            if time_difference < tempo_minimo:

                ip_data["slow_down_count"] += 1
                # limite de requisiçoes por tempo_minimo
                if ip_data["slow_down_count"] > 5:
                    coment = "chegou ao limite de requisições por minuto"
            else:
                # Resetando o slow_down_count
                ip_data["slow_down_count"] = 0
        else:
            # ------------ block by request_time_limit ------------

            # Se a diferença de tempo for menor que 10 segundos            
            #Nota: no futuro modificar para o contador tambem usar o fingerprint nao so o IP para bloquiar o acesso
            if time_difference < 10:
                
                ip_data["request_time_limit_count"] += 1

                # limite de vezes em que se pode passar dos segundos minimos entre requisiçoes
                if ip_data["request_time_limit_count"] > 5:

                    # aumenta no nivel de suspeita e adiciona um coment
                    ip_data["suspicion_Level"] += 3
                    coment = "Request time limit: Alert, "
                    
                    # cria e adicina o log
                    log = Request_Log(tempo_atual, ip_address, PATH, user_agent, New_fingerprint, coment)
                    log.create_log()

                    # ativa o modo slow_down que limita a quantidade de requisições por tempo_minimo
                    # normalmente 1 minuto
                    ip_data["slow_down"] = "on"

                    # O False indica que o acesso nao passou na verificaçao de segurança
                    return (False,coment)
            else:
                # volta o contador para 0 so vai ser bloquiado se for varias vezes seguidas
                ip_data["request_time_limit_count"] = 0
                # atualiza o ultimo tempo de requisição
        ip_data["last_request_time"] = tempo_atual.strftime('%Y-%m-%d %H:%M:%S')

    # ------------------ request limits per IP ------------------    

    # aumenta o contador de requisições
    ip_data["request_count"] += 1

    # Se passar de um certo número de requests, bloqueia o acesso
    if ip_data["request_count"] > 5000: # limite de requisiçoes por IP atualment => 50
        coment = "Chegou a quantidade maxima de requisições por IP"

        # cria e adicina o log
        log = Request_Log(tempo_atual, ip_address, PATH, user_agent, New_fingerprint, coment)
        log.create_log()

        add_IP_data_to_DB(ip_address, ip_data)

        # O False indica que o acesso nao passou na verificaçao de segurança
        return (False,coment)
        

    # ------------------ Agent blocker ------------------

    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if re.search(r'\bbot\b', user_agent, re.IGNORECASE) or re.search(r'\bscraper\b', user_agent, re.IGNORECASE):
        coment += "agents_check: alert, "
        ip_data["suspicion_Level"] += 10
    
    # se o agente for "headless" nao vai ter acesso ao site
    if re.search(r'\bheadless\b', user_agent, re.IGNORECASE):
        coment += "agents_headless: alert, "
        ip_data["suspicion_Level"] += 10
    

    # ------------------ verifica se o IP esta em uma black list ou yellow list ------------------    

    # bloqueia os IPs que estiverem na black list ou na yellow list e adiciona um comentario
    if ip_address in black_list_IP or ip_address in yellow_list_IP:
        coment = "IP esta em uma das listas de bloqueio"

        # cria e adicina o log
        log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
        log.create_log()
        
        # O False indica que o acesso nao passou na verificaçao de segurança
        return (False,coment)

# ------------------ no final de tudo ------------------ 

    # se o nivel de suspeita passar de 5, ativa o slow_down
    if ip_data["suspicion_Level"] > 5:
        # ativa o modo slow_down que limita a quantidade de requisições por tempo_minimo
        # normalmente o tempo_minimo = 1 minuto
        # Nota: isso e apenas para um IP especifico
        ip_data["slow_down"] = "on"
    # atualizar o IP_Data no MongoDB
    add_IP_data_to_DB(ip_address, ip_data)
     
    if ip_data["suspicion_Level"] >= 10:
        
        # O False indica que o acesso nao passou na verificaçao de segurança
        return (False,coment)

    # se o acesso passou por todas as verificacoes, o acesso pode ser autorizado
    Final_coment = "Acesso autorizado"

    # cria e adicina o log no MongoDB
    log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    log.create_log()
    # O True indica que o acesso passou na verificaçao de segurança

    return (True,Final_coment)