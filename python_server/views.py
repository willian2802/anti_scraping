from flask import Blueprint, render_template, request, abort

views = Blueprint(__name__, 'views')


black_list_IP = []
yellow_list_IP = []
access_log = {}  #dicionário para registrar as requisições

@views.route('/')
def render_index():
    # isso renderiza o index.html da pasta templates e a pagina do captcha
    return render_template('index.html')


    
@views.route('/cofe_shop')
def cofe_page():
    # isso renderiza a pagina cof_page da pasta templates 
    return render_template('cof_page.html')

access_log = {}
@views.route('/descobrir_IP')
def descobrir_IP():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    if user_ip not in access_log:
        access_log[user_ip] = []
    access_log[user_ip].append(request.path)

    #  se passar o limite de request o ip vai ser bloqueado
    if len(access_log[user_ip]) > 100:  # Ajuste o limite conforme necessário
        return abort(403)  # Bloqueia IPs com muitas requisições

    return f"User IP: {user_ip}, User Agent: {user_agent}, Access Log: {access_log}"

