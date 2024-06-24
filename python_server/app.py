from datetime import datetime
from flask import Flask, request, abort
from views import views


app = Flask(__name__)

# para acessar essa pagina e "/views" se quizer depois acessar outra pagina /views/home etc...
app.register_blueprint(views, url_prefix='/views')


# --------------------------- block bots ---------------------------
black_list_IP = ["192.168.0.1", "192.168.0.2"]
yellow_list_IP = []
green_list_IP = []

access_log = {}  #dicionário para registrar as requisições

@app.route('/')
def block_user_for():

    # Define the list of blocked IP addresses
    ip_address = request.remote_addr

    if ip_address not in access_log:
        access_log[ip_address] = []
    access_log[ip_address].append(request.path)

    #  se passar o limite de request o ip vai ser bloqueado
    if len(access_log[ip_address]) > 10:  # Ajuste o limite conforme necessário
        return abort(403)  # Bloqueia IPs com muitas requisições

    # bloqueia os agents que tenhan o nome "bot" ou "scraper"
    user_agent = request.headers.get('User-Agent')
    if "bot" in user_agent.lower() or "scraper" in user_agent.lower():
        return abort(403)
    
    # se o agente for "headless" nao vai ter acesso ao site    
    if "Headless" in user_agent:
        return abort(403)
    
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
    
    if ip_address not in access_log:
        access_log[ip_address] = []
    access_log[ip_address].append(request.path)
    
    #  se passar o limite de request o ip vai ser bloqueado
    if len(access_log[ip_address]) > 100:  # Ajuste o limite conforme necessário
        return abort(403)  # Bloqueia IPs com muitas requisições


@app.route('/endereco-de-processamento', methods=['POST'])
def trap_activated():
    ip_address = request.remote_addr

    # pega o tempo do request
    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')

    #adiciona o ip na yellow list
    yellow_list_IP.append(request.remote_addr)
    return f"Time: {current_time}, User IP:{ip_address}"

if __name__ == '__main__':
    app.run(debug=True)



