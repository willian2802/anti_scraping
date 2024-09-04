from flask import Flask, request, jsonify, abort
from views import views

from datetime import datetime
from functools import wraps


from functions import Logs

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessário para usar sessões
# app.config["MONGO_URI"] = "mongodb://localhost:27017/sample_mflix"


# para acessar essa pagina e "/views" se quizer depois acessar outra pagina /views/home etc...
app.register_blueprint(views, url_prefix='/views')

# +--------------------------- lists ---------------------------

from MongoDB import add_to_ConfigList


# -------------------------------- Console log --------------------------------

# qualquer um que entrar nesse endereço o servidor vai enviar os Logs para ele
@app.route('/just-logs', methods=['GET'])
def get_logs():
    # Retorna a lista de logs em formato JSON
    return jsonify(Logs)


# -------------------------------- movement and mouse events tracker --------------------------------

def is_smooth_and_constant(movements):
    # Verifica se os movimentos são muito suaves e constantes
    threshold = 2  # Pixels de diferença mínima para considerar como movimento humano
    smooth_movements = sum(
        1 for i in range(1, len(movements))
        if abs(movements[i]['x'] - movements[i-1]['x']) < threshold and
           abs(movements[i]['y'] - movements[i-1]['y']) < threshold
    )
    return smooth_movements > len(movements) * 0.9  # Se mais de 90% dos movimentos forem suaves

def is_frequency_high(movements):
    # Verifica se a frequência dos eventos de movimento é muito alta
    timestamps = [m['timestamp'] for m in movements]
    intervals = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
    average_interval = sum(intervals) / len(intervals)
    return average_interval < 10  # Se o intervalo médio for menor que 10ms

def has_human_variation(movements):
    # Verifica se há variação humana nos movimentos
    directions = [
        (movements[i]['x'] - movements[i-1]['x'], movements[i]['y'] - movements[i-1]['y'])
        for i in range(1, len(movements))
    ]
    direction_changes = sum(
        1 for i in range(1, len(directions))
        if directions[i] != directions[i-1]
    )
    return direction_changes > len(directions) * 0.5  # Se mais de 50% das direções mudarem



@app.route('/track_interaction', methods=['POST'])
def track_interaction():
    interaction_data = request.json
    print('Dados de interação recebidos:')

    track_movements = 0

    if interaction_data['event'] == 'mousemove':
        movements = interaction_data['movements']
        if is_smooth_and_constant(movements):
            #'Interação suspeita detectada: Movimentos muito suaves e constantes'
            print('Interação suspeita detectada: Movimentos muito suaves e constantes')
            track_movements += 1
        elif is_frequency_high(movements):
            #'Interação suspeita detectada: Frequência de eventos muito alta'
            print('Interação suspeita detectada: Frequência de eventos muito alta')
            track_movements += 1
        elif not has_human_variation(movements):
            #'Interação suspeita detectada: Falta de variação humana nos movimentos'
            print('Interação suspeita detectada: Falta de variação humana nos movimentos')
            track_movements += 1
        else:
            #'Interação parece ser humana'
            track_movements = True

    if track_movements >= 2:
        abort(444, 'Interação suspeita detectada: Movimonto não humano')
        
    return jsonify(status="success"), 200



# -------------------------------- honneypot --------------------------------
@app.route('/endereco-de-processamento', methods=['POST'])
def trap_activated():
    ip_address = request.remote_addr
    # pega o tempo do request
    c = datetime.now()
    current_time = c.strftime('%H:%M:%S')

    #adiciona o ip na yellow list
    add_to_ConfigList(ip_address, "black_list_IP")

    return f"Ha, It's a TRAP!!!!!! Seu IP: {ip_address}, no horario: {current_time}, esta agora bloqueado de acessar o site"

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, session
# from flask_session import Session

# app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# @app.route("/")
# def index():
#     session["authenticated"] = True
#     return "Olá, mundo!"

# @app.route("/outro")
# def outro():
#     if session["authenticated"]:
#         return "Você está autenticado!"
#     else:
#         return "Você não está autenticado!"
