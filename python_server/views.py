from collections import defaultdict
from flask import Blueprint, render_template, request


from app import block_user_for
# from .block_user_for import block_user_for

views = Blueprint(__name__, 'views')


black_list_IP = []
yellow_list_IP = []

@views.route('/')
def render_index():

    block_user_for()
    # isso renderiza o index.html da pasta templates e a pagina do captcha
    return render_template('index.html')


    
@views.route('/cofe_shop')
def cofe_page():
    # isso renderiza a pagina cof_page da pasta templates 
    return render_template('cof_page.html')

logs = []
User_information = []
@views.route('/descobrir_IP')
def descobrir_IP():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    user_info = {
            'user_ip': "121.121.121.121",
            'user_agent': user_agent,
        }

    # verifica se ja tem as informaçoes do usario
    # se nao adiciona as informaçoes no user_info
    if user_info not in User_information:
        logs.append(user_info)
    
    # generate a log
    log = {
        'user_ip': user_ip,
        'user_agent': user_agent,
    }
    logs.append(log)
    

    # Add the user's IP address to the list yellow_list_IP
    # if the request is more than a certain number of times

    # Dictionary to store the count of each IP address in the logs
    ip_count = defaultdict(int)

    if user_ip not in yellow_list_IP:
        for log in logs:
            ip_address = log['user_ip']
            ip_count[ip_address] += 1

        if ip_count[ip_address] > 5:
            yellow_list_IP.append(user_ip)

    return f"user_ip: {user_ip}, user_agent: {user_agent}, logs list: {logs}"


# como importar a funçao do app.py pro views.py da conflito ja que ambos estao importando uns
# dos outros talves seja melhor colocar as funçoes em utils.py so importar pra quanndo eu precisar

# utils.py

# def block_user_for():
#     # your code here
#     pass


# # views.py

# from flask import Blueprint, render_template, request
# from utils import block_user_for

# views = Blueprint(__name__, 'views')

# @views.route('/')
# def render_index():
#     block_user_for()
#     return render_template('index.html')

# # app.py

# from flask import Flask
# from views import views
# from utils import block_user_for

# app = Flask(__name__)

# app.register_blueprint(views, url_prefix='/views')

# # views.py

# from flask import Blueprint, render_template, request
# from utils import block_user_for

# views = Blueprint(__name__, 'views')

# @views.route('/')
# def render_index():
#     block_user_for()
#     return render_template('index.html')