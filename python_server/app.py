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


# +--------------------------- autenticação ---------------------------

@app.route('/submit_captcha', methods=['POST'])
def submit_captcha():
    data = request.get_json()
    user_text = data.get('userText')
    # Processa o user_text como necessário
    print(f"Received user text: {user_text}")
    return jsonify({'status': 'success'})



# Função de verificação de autenticação

#verifica se a chave 'authenticated' está presente no dicionário session. 
# Se estiver presente, significa que o usuário está autenticado. 
# A sessão é um dicionário que o Flask usa para armazenar dados entre requisições.
def is_authenticated():
    return 'authenticated' in session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('views'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/views', methods=['GET', 'POST'])
def views():
    if request.method == 'POST':
        captcha = request.form.get('captchahash')

        # Aqui você deve implementar sua lógica de autenticação
        # Por exemplo, verificar o usuário e a senha
        # Se autenticado com sucesso:
        session['authenticated'] = True
        return redirect(url_for('home'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

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



