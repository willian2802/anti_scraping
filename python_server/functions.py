import hashlib, platform, os, re
from collections import defaultdict
from flask import request, session, redirect, url_for
from datetime import datetime
from functools import wraps

# MongoDB
from MongoDB import add_log_to_DB, add_IP_data_to_DB, get_ip_data_from_db, check_if_is_in


# geolication
import requests


# import tkinter as tk

# to use this i need to install screeninfo and geopy
# from screeninfo import get_monitors

# -------------------------------------------- Securety Config --------------------------------------------

# Limite do nivel de suspeita antes de ser bloqueado
suspicion_limit = 10

# Tempo minimo de tolerancia entre as requisições
# mandar multiplas requisiçoes passando do limite de tempo ira levar ao eventual bloqueio
time_limit = 10

# +--------------------------- lists ---------------------------

# black_list_IP = ["192.168.0.44", "192.168.0.75"]
# yellow_list_IP = []
# green_list_IP = []

# contry_black_list = ["China","India","Brazil","Russia"]


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
    

#  ------------------------------ mouse movement --------------------------------

def movement_is_from_a_bot(result):

    ip_address = request.remote_addr

    ip_data = get_ip_data_from_db(ip_address)

    # adiciona o IP_data no mongoDB, o ip_address vai ser o "_id" do objeto no DB
    add_IP_data_to_DB(ip_address, new_ip_data)

    if result == True:
        ip_data

# ------------------------------ verifica se e uma VPN ou uma proxy --------------------------------
# usando a API do IPQualityScore

# def is_anonymous_ip(ip_address):
#     api_key = "YOUR_API_KEY"  # Substitua pela sua chave de API do IPQualityScore
#     url = f"https://ipqualityscore.com/api/json/ip/{api_key}/{ip_address}"

#     response = requests.get(url)
#     data = response.json()

#     if data['proxy'] or data['vpn']:
#         return True
#     return Fals5e



# def detect_vpn_proxy(ip_address):
#     api_url = f"https://api.ipify.org?format=json&ip={ip_address}"
#     response = requests.get(api_url)
#     data = response.json()
#     if data["proxy"] or data["vpn"]:
#         return True
#     return False

# # Example usage:
# ip_address = "8.8.8.8"
# if detect_vpn_proxy(ip_address):
#     print("VPN or proxy detected!")
# else:
#     print("No VPN or proxy detected.")

# ------------------------------ Geolocalização --------------------------------

def get_ip_location(ip):
    ip_to_locate = ip

    response = requests.get('http://ip-api.com/json/' + ip_to_locate + '?fields=country').json()

    return(response)

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
    ip_address = "157.3.5.16"
    user_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    PATH = request.path
    user_agent = request.headers.get('User-Agent')

    # uma descriçao para o log ou outras informaçoes uteis
    coment = "None"

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

    # ------------------ block requests com muitas requisições em um curto período de tempo e verifica o fingerprint ------------------

    # Obtendo o tempo atual como objeto datetime
    # nao funciona usando o user_time 
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
            # se passar de um certo limite de requisições o acesso é suspenso
            "request_count": 0,
            # request_time_limit_count => quantidade de requisições em um curto período de tempo sequidas
            "request_time_limit_count": 0,
            # last_request_time => tempo da requisição mais recente
            "last_request_time": tempo_atual.strftime('%Y-%m-%d %H:%M:%S'),
            "time_to_delete": 24,
            "slow_down": "off",
            "slow_down_count": 0
        }

        # adiciona o IP_data no mongoDB, o ip_address vai ser o "_id" do objeto no DB
        add_IP_data_to_DB(ip_address, new_ip_data)

        # pega o IP_data no mongoDB usando o IP
        ip_data = get_ip_data_from_db(ip_address)
        # quando o IP_data e criado e adicionado DB o tempo de acesso do IP e 12:00
        # assim evitando erro com o "slow_down" mode
        ip_data["last_request_time"] = tempo_atual.replace(hour=12, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')


    else:
        # pega o IP_data no mongoDB usando o IP
        ip_data = get_ip_data_from_db(ip_address)
        # para iniciar de novo a verificaçao de segurança
        # e preciso redefinir o nivel de suspeita
        ip_data["suspicion_Level"] = 0

        # verifica se o pais esta na blacklist
        # se retornar True significa que esta na lista
        if check_if_is_in(ip_data['Country'], "country_black_list") == True:

            coment = "Acesso não autorizado ao pais em que voce esta localizado"
            # cria e adicina o log no DB
            log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
            log.create_log()
            return (False, coment)
        
        if check_if_is_in(ip_data['Country'], "country_yellow_list") == True:

            ip_data["suspicion_Level"] += 2
            coment += "Country: Alert, "

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
            if time_difference <= time_limit:
                
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
        coment += "agents_check: RED ALERT, "
        ip_data["suspicion_Level"] += 10
    
    # se o agente for "headless" nao vai ter acesso ao site
    if re.search(r'\bheadless\b', user_agent, re.IGNORECASE):
        coment += "agents_headless: RED ALERT, "
        ip_data["suspicion_Level"] += 10
    

# ------------------ no final de tudo ------------------ 

    # se o nivel de suspeita passar de 5, ativa o slow_down
    if ip_data["suspicion_Level"] > 5:
        # ativa o modo slow_down que limita a quantidade de requisições por tempo_minimo
        # normalmente o tempo_minimo = 1 minuto
        # Nota: isso e apenas para um IP especifico
        ip_data["slow_down"] = "on"
    # atualizar o IP_Data no MongoDB
    add_IP_data_to_DB(ip_address, ip_data)


    # se o nivel de suspeita for maior ou igual ao suspicion_limit
    if ip_data["suspicion_Level"] >= suspicion_limit:
        
        # O False indica que o acesso nao passou na verificaçao de segurança
        return (False,coment)

    # se o acesso passou por todas as verificacoes, o acesso pode ser autorizado
    Final_coment = "Acesso autorizado"

    # cria e adicina o log no MongoDB
    log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    log.create_log()
    # O True indica que o acesso passou na verificaçao de segurança

    return (True,Final_coment)