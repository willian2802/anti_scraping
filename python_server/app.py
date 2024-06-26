import hashlib
from flask import Flask, request, abort
from views import views
from datetime import datetime, timedelta

app = Flask(__name__)

# para acessar essa pagina e "/views" se quizer depois acessar outra pagina /views/home etc...
app.register_blueprint(views, url_prefix='/views')

# +--------------------------- lists ---------------------------

black_list_IP = ["192.168.0.1", "192.168.0.2"]
yellow_list_IP = []
green_list_IP = []

access_log = {}  #dicionário para registrar as requisições

# --------------------------- Logs Class ---------------------------
class Request_Log:
    def __init__(self, current_time, ip_address, path, agent, hash_code):
        self.current_time = current_time
        self.ip_address = ip_address
        self.path = path
        self.agent = agent
        self.hash_code = hash_code

    def __create__(self):
        access_log[self.current_time].append(self.current_time)
        access_log[self.ip_address].append(self.ip_address)
        access_log[self.path].append(self.path)
        access_log[self.agent].append(self.agent)
        access_log[self.hash_code].append(self.hash_code)

    def __show__(self):
        return f"Current Time: {self.current_time}, IP: {self.ip_address}, Path: {self.path}, Agent: {self.agent}, Hash Code: {self.hash_code}"

    def __remove__(self):
        access_log[self.ip_address].remove(self.path)
        

# --------------------------- block bots ---------------------------


@app.route('/')
def block_user_for():

    ip_address = request.remote_addr

    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if "Chrome" in user_agent.lower() or "scraper" in user_agent.lower():
        return "Access denied. Bots or scrapers are not pertmitted" 
    
    # se o agente for "headless" nao vai ter acesso ao site    
    if "Headless" in user_agent:
        return "Access denied. headless are not pertmitted" 
    
    if ip_address not in access_log:
        access_log[ip_address] = []
    access_log[ip_address].append(request.path)
    
    #  se passar o limite de request o ip vai ser bloqueado e adicionado na yellow list
    if len(access_log[ip_address]) > 100:  # Ajuste o limite conforme necessário
        yellow_list_IP.append(request.remote_addr)
        return abort(403)  # Bloqueia IPs com muitas requisições

    # Check if the user's IP address is in the list of blocked IP addresses
    if ip_address in black_list_IP:
        return f"Access denied. UserIP:{ip_address}, You are blocked from accessing this page."
    
# -------------------------------- update_access_log and list_IPs--------------------------------
# @app.route('/IPs_list')
# def list_IPs_updated():

#     ip_address = request.remote_addr
#     if ip_address not in access_log:
#         access_log[ip_address] = []
#     # tempo_para_limpar = datetime.now() - timedelta(hours=6)

#     # for ip_user in access_log: 
#     #     if ip_user.current_time > tempo_para_limpar:
#     #         access_log[ip_address].remove("/endereco-de-processamento")
#     #         access_log[ip_address].remove("12:14:14")

#     # access_log[ip_address].append("/endereco-de-processamento")
#     # access_log[ip_address].append("12:14:14")
#     # access_log[ip_address].append("11:14:14")


#     return f"Access Log: {access_log}"


# -------------------------------- honneypot --------------------------------
@app.route('/endereco-de-processamento', methods=['POST'])
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
# --------------------------- fingerprint ---------------------------
@app.route('/fingerprint')
def generate_ip_fingerprint() -> str:

    user_Ip = request.remote_addr
    user_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_agent = request.headers.get('User-Agent')

    # Combina os dois IPs em uma única string
    combined_data = f"{user_Ip}-{user_time}-{user_agent}"
    # Cria um objeto hash SHA-256
    hash_object = hashlib.sha256()
    # Atualiza o objeto hash com os dados combinados (codificados em bytes)
    hash_object.update(combined_data.encode('utf-8'))
    # Obtém o hash hexadecimal
    fingerprint = hash_object.hexdigest()
    return fingerprint



if __name__ == '__main__':
    app.run(debug=True)



