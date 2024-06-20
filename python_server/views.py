from flask import Blueprint, render_template, request, abort

views = Blueprint(__name__, 'views')


@views.route('/')
def block_user_for():

    # Define the list of blocked IP addresses
    ip_address = request.remote_addr
    blocked_ips = ["192.168.0.1", "192.168.0.2"]

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

    # Check if the user's IP address is in the list of blocked IP addresses
    if ip_address in blocked_ips:        
        return f"Access denied. UserIP:{ip_address}, You are blocked from accessing this page."
    else:
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


