from flask import Flask, request, jsonify, redirect, url_for,session
from views import views
from datetime import datetime
from functools import wraps


from functions import Logs

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessário para usar sessões


# para acessar essa pagina e "/views" se quizer depois acessar outra pagina /views/home etc...
app.register_blueprint(views, url_prefix='/views')

# +--------------------------- lists ---------------------------

from functions import yellow_list_IP, green_list_IP, black_list_IP


# # +--------------------------- autenticação ---------------------------

# @app.route('/submit_captcha', methods=['POST'])
# def submit_captcha():

#     print("submit_captcha is on!!!") 

#     if request.method == 'POST':
#         # pega a resposta do captcha do usuario    
#         data = request.get_json()
#         # reposta do captcha do usuario
#         user_text = data.get('userText')
#         right_captcha = data.get('right_captcha')

#         print(user_text)
#         print(right_captcha)
#         # Se autenticado com sucesso
        
#         if right_captcha == True:
            
#             session['authenticated'] = True
#             return('captcha autenticado com sucesso')
#         else:
#             session['authenticated'] = False
#             return redirect(url_for('views.render_index'))

# -------------------------------- Console log --------------------------------

# qualquer um que entrar nesse endereço o servidor vai enviar os Logs para ele
@app.route('/just-logs', methods=['GET'])
def get_logs():
    # Retorna a lista de logs em formato JSON
    return jsonify(Logs)


# -------------------------------- honneypot --------------------------------
@app.route('/endereco-de-processamento', methods=['POST'])
def trap_activated():
    ip_address = request.remote_addr
    # pega o tempo do request
    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')

    #adiciona o ip na yellow list
    yellow_list_IP.append(ip_address)

    return f"Ha, It's a TRAP!!!!!! Seu IP: {ip_address}, no horario: {current_time}, esta agora bloqueado de acessar o site"

if __name__ == '__main__':
    app.run(debug=True)



