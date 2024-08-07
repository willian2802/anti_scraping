from flask import Blueprint, render_template, request
from functions import Securety_check,login_required

views = Blueprint(__name__, 'views')


# black_list_IP = []
# yellow_list_IP = []


@views.route('/')
def render_index():

    # roda as funçoes que verificao se e um bot ou nao se for entao bloqueia o acesso
    Securety_check()
    result, comment = Securety_check()

    # verifica se a function retorna False isso significa que o acesso foi bloqueado
    if result == False:

        return f"{comment}"

    # isso renderiza o index.html da pasta templates e a pagina do captcha
    return render_template('index.html')


# renderiza o visualizador de Logs
@views.route('/nothing_here')
def logs_console():
    return render_template('nothing_here.html')
    
@views.route('/cofe_shop')
@login_required
# antes de ativar a funçao, ele vai rodar a funçao Login_required
# que verifica se o usuario foi autenticado se sim ele passa se nao ele volta pro index que e o captcha
def cofe_page():
    # roda as funçoes que verificao se e um bot ou nao se for entao bloqueia o acesso
    Securety_check()
    result, comment = Securety_check()

    # verifica se a function retorna False isso significa que o acesso foi bloqueado
    if result == False:

        return f"{comment}"

    # isso renderiza a pagina cof_page da pasta templates 
    return render_template('cof_page.html')


# apenas para teste
@views.route('/descobrir_IP')
def descobrir_IP():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    return f"user_ip: {user_ip}, user_agent: {user_agent}, "
