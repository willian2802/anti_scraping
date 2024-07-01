import hashlib
from flask import Flask, request, abort
from datetime import datetime, timedelta


# +--------------------------- lists ---------------------------

black_list_IP = ["192.168.0.1", "192.168.0.2"]
yellow_list_IP = []
green_list_IP = []

access_log = {}  #dicionário para registrar as requisições


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
    user_agent = request.headers.get('User-Agent')
    PATH = request.path
    
    # uma descriçao para o log ou outras informaçoes uteis
    coment = "None"


    # ------------------ Create finger-print ------------------
    # lembrando que o fingerprint como so nos interesa e criar um jeito de identificar as
    # maquinas que estao tentando acessar o site, request_time e user_agent e por fim o IP
    # pode nao ser a melhor escolha para faazer o fingerprint
    # tamanho da tela e o sistema operacional etc... pode uma melhor escolha
     
    # Combina os dois IPs em uma única string
    combined_data = f"{ip_address}-{user_time}-{user_agent}"
    # Cria um objeto hash SHA-256
    hash_object = hashlib.sha256()
    # Atualiza o objeto hash com os dados combinados (codificados em bytes)
    hash_object.update(combined_data.encode('utf-8'))
    # Obtém o hash hexadecimal
    New_fingerprint = hash_object.hexdigest()


    # bloqueia os IPs que estiverem na black list ou na yellow list
    if ip_address in black_list_IP or ip_address in yellow_list_IP:
        coment = "IP esta em uma das listas de bloqueio" 
        return abort(403)

    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if "bot" in user_agent.lower() or "scraper" in user_agent.lower():
        coment = "bloquiado por causa do agente"
        return abort(403)
    
    # se o agente for "headless" nao vai ter acesso ao site
    if "Headless" in user_agent:
        coment = "bloquiado por usar agente headless"
        return abort(403)
    
    if ip_address not in access_log:
        access_log[ip_address] = []
    access_log[ip_address].append(request.path)
    
    # #  se passar o limite de request o ip vai ser bloqueado e adicionado na yellow list
    # if len(access_log[ip_address]) > 100:  # Ajuste o limite conforme necessário
    #     yellow_list_IP.append(request.remote_addr)
    #     return abort(403)  # Bloqueia IPs com muitas requisições

    

    log = Request_Log(user_time, ip_address, PATH, user_agent, New_fingerprint, coment)
    log.create_log()
    print(log)

    
# -------------------------------- update_access_log and list_IPs--------------------------------
def list_IPs_updated():

    ip_address = request.remote_addr
    if ip_address not in access_log:
        access_log[ip_address] = []
    # tempo_para_limpar = datetime.now() - timedelta(hours=6)

    # for ip_user in access_log: 
    #     if ip_user.current_time > tempo_para_limpar:
    #         access_log[ip_address].remove("/endereco-de-processamento")
    #         access_log[ip_address].remove("12:14:14")

    # access_log[ip_address].append("/endereco-de-processamento")
    # access_log[ip_address].append("12:14:14")
    # access_log[ip_address].append("11:14:14")


    return f"Access Log: {Logs}"

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