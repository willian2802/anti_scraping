from flask import Flask, request, abort
from views import views


app = Flask(__name__)

# para acessar essa pagina e "/views" se quizer depois acessar outra pagina /views/home etc...
app.register_blueprint(views, url_prefix='/views')


# --------------------------- block bots ---------------------------
    
@app.route('/endereco-de-processamento', methods=['POST'])
def process_form():
    return "Its a TRAP!!!"

access_log = {}
@app.route('/endereco-de-processamento', methods=['GET', 'POST'])
def handle_request():
    ip = request.remote_addr
    if ip not in access_log:
        access_log[ip] = []
    access_log[ip].append(request.path)
    
    #  se passar o limite de request o ip vai ser bloqueado
    if len(access_log[ip]) > 100:  # Ajuste o limite conforme necessário
        return abort(403)  # Bloqueia IPs com muitas requisições
    
    # Lógica normal de processamento
    return "Requisição processada com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)



