import hashlib
from flask import Flask, request, abort
from views import views
from datetime import datetime, timedelta



app = Flask(__name__)

# para acessar essa pagina e "/views" se quizer depois acessar outra pagina /views/home etc...
app.register_blueprint(views, url_prefix='/views')

# +--------------------------- lists ---------------------------

black_list_IP = ["192.168.0.1", "192.168.0.2"]
yellow_list_IP = ["127.0.0.1", "127.0.0.2"]
green_list_IP = []

access_log = {}  #dicionário para registrar as requisições        

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
    yellow_list_IP.append(ip_address)

    return f"Seu IP: {ip_address}, no horario: {current_time}, esta agora bloqueado de acessar o site"

if __name__ == '__main__':
    app.run(debug=True)



