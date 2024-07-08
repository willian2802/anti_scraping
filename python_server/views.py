from flask import Blueprint, render_template, request
from functions import block_user_for

views = Blueprint(__name__, 'views')


# black_list_IP = []
# yellow_list_IP = []

@views.route('/')
def render_index():

    # roda as funçoes que verificao se e um bot ou nao se for entao bloqueia o acesso
    block_user_for()
    result, comment = block_user_for()

    # verifica se a function retorna true isso significa que o acesso foi bloqueado
    if result == True:

        return f"{comment}"

    # isso renderiza o index.html da pasta templates e a pagina do captcha
    return render_template('index.html')


@views.route('/nothing_here')
def logs_console():

    return render_template('nothing_here.html')
    
@views.route('/cofe_shop')
def cofe_page():
    # roda as funçoes que verificao se e um bot ou nao se for entao bloqueia o acesso
    block_user_for()
    result, comment = block_user_for()

    # verifica se a function retorna true isso significa que o acesso foi bloqueado
    if result == True:

        return f"{comment}"

    # isso renderiza a pagina cof_page da pasta templates 
    return render_template('cof_page.html')


# apenas para teste
@views.route('/descobrir_IP')
def descobrir_IP():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    return f"user_ip: {user_ip}, user_agent: {user_agent}, "
