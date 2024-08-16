# ------------------------ selenium ------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time, random


#https://sites.google.com/chromium.org/driver/

# Specify the path to chromedriver.exe
# By the love of God do not change the "S" from "Service" this broken something
Service = Service(executable_path="D:/IEFP_curso/IEFP_Projects/seleniun_test/chromedriver.exe")
driver = webdriver.Chrome(service=Service)



def test_honeypot():
    try:
        # ------------------------ honeypot test ------------------------
        # Acesse a página inicial
        driver.get('http://127.0.0.1:5000/views/')

        # usa o wait para esperar ao inves do time.sleep()
        # por que o time.sleep() da erro
        wait = WebDriverWait(driver, 10)
        nome_input = wait.until(EC.presence_of_element_located((By.NAME, 'nome')))

        # inseri no input nome => "willian souza"
        nome_input.send_keys('willian souza')

        # Wait for one second
        time.sleep(1)

        # encontra o input com o nome enviar e clica
        enviar_input = driver.find_element(By.NAME, 'enviar')
        enviar_input.click()

        # Aguardar a resposta do login
        time.sleep(50)

        # Após a autenticação, tente acessar outra página para testar a medida anti-scraping
        # driver.get('https://willian.pythonanywhere.com/views/cofe')

        # Verificar o conteúdo da página
        page_content = driver.page_source

        # Aqui você pode adicionar verificações para ver se a página foi carregada corretamente
        if 'conteudo_especifico' in page_content:
            print("Página acessada com sucesso, medidas anti-scraping não detectadas.")
        else:
            print("Não foi possível acessar a página, medidas anti-scraping detectadas.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # Fechar o navegador
        driver.quit()


def test_multiple_request():
    # numero de requisições
    num_requests = 10

    # tempo entre as requisiçoes
    delay = 0.5

    try:
        # Loop through the number of requests
        for _ in range(num_requests):
            # Open the webpage
            driver.get("https://willian.pythonanywhere.com/views")

            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Do something with the page (e.g., extract data)

            # tempo entre as requisições
            time.sleep(delay)

            wait = WebDriverWait(driver, 10)

        # Verificar o conteúdo da página
        page_content = driver.page_source

        # Aqui você pode adicionar verificações para ver se a página foi carregada corretamente
        if 'conteudo_especifico' in page_content:
            print("Página acessada com sucesso, medidas anti-scraping não detectadas.")
        else:
            print("Não foi possível acessar a página, medidas anti-scraping detectadas.")

    except Exception as e:
        print(f"An error occurred: {e}")


# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 bot (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0  (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 scraping (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/5.0 bot (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
]

def test_agensts_detection():
    # teste para a detecção de agente e fingerprint
    try:

        # Loop through the list of user agents
        for user_agent in user_agents:
            # Create a new WebDriver instance with the current user agent
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={user_agent}')
            current_driver = webdriver.Chrome(options=options)

            # Open the webpage
            current_driver.get("https://willian.pythonanywhere.com/views")

            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Do something with the page (e.g., extract data)
            
            # Wait for the delay before accessing the next page with the next user agent
            time.sleep(5)

            # Close the browser
            current_driver.quit()

        # conteúdo da página
        page_content = current_driver.page_source

        # Aqui você pode adicionar verificações para ver se a página foi carregada corretamente
        if 'conteudo_especifico' in page_content:
            print("Página acessada com sucesso, medidas anti-scraping não detectadas.")
        else:
            print("Não foi possível acessar a página, medidas anti-scraping detectadas.")
 

    except Exception as e:
        print(f"An error occurred: {e}")

def test_mouse_movement():
    
    # Acesse a página inicial
    driver.get('http://127.0.0.1:5000/views/')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Execute o Chrome em modo headless (sem janela gráfica)

    # Inicializar ActionChains
    actions = ActionChains(driver)

    # Função para simular movimentos do mouse
    def simulate_mouse_movements():
        body = driver.find_element('body')
        for _ in range(100):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            actions.move_by_offset(x_offset, y_offset).perform()
            time.sleep(0.05)
            actions.move_to_element(body).perform()

    # Função para simular cliques
    def simulate_clicks():
        for _ in range(10):
            x_offset = random.randint(0, driver.execute_script("return window.innerWidth"))
            y_offset = random.randint(0, driver.execute_script("return window.innerHeight"))
            actions.move_by_offset(x_offset, y_offset).click().perform()
            time.sleep(0.2)

    # Função para simular rolagem
    def simulate_scroll():
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(0.2)
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(0.2)
    
    # Executar simulações
    simulate_mouse_movements()
    simulate_clicks()
    simulate_scroll()

    time.sleep(50000)


def simulate_human_mouse_movements(driver, duration):
    actions = ActionChains(driver)
    body = driver.find_element(By.TAG_NAME, 'body')
    start_time = time.time()
    window_width = driver.execute_script("return window.innerWidth")
    window_height = driver.execute_script("return window.innerHeight")
    
    while time.time() - start_time < duration:
        x_offset = random.randint(100, window_width - 100)
        y_offset = random.randint(100, window_height - 100)
        actions.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.5, 2.0))
        actions.move_to_element(body).perform()
        if random.random() < 0.1:
            actions.click().perform()

# Test function
def test_mouse_movement2():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000/views/')
    simulate_human_mouse_movements(driver, 50)  # Reduced duration for testing
    driver.quit()

test_mouse_movement()



# Configurações para diferentes máquinas
machines = [
    {"window_size": "1920,1080", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"window_size": "1366,768", "user_agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"},
    {"window_size": "1440,900", "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"window_size": "2560,1440", "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"window_size": "375,812", "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"}
]

# URL do seu arquivo HTML
url = "file:///caminho/para/seu/arquivo.html"  # Atualize o caminho para o seu arquivo HTML

# Simular interação para cada máquina
for machine in machines:
    simulate_interaction(machine["window_size"], machine["user_agent"], url)

# ------------------------------ Executar o teste --------------------------------
# test_honeypot()
# test_multiple_request()
# test_agensts_detection()

# test_acesso_por_pais('BR', 'https://willian.pythonanywhere.com/views/cofe_shop')
#test_mouse_movement()

# # Lista de proxies organizados por país
# proxies = {
#     "France": "fr.proxy.example:8080",
#     "Italy": "it.proxy.example:8080",
#     "Brazil": "br.proxy.example:8080",
#     "China": "cn.proxy.example:8080"
# }

# # Configurar o proxy
# def configure_proxy(country):
#     proxy = Proxy()
#     proxy.proxy_type = ProxyType.MANUAL
#     proxy.http_proxy = proxies[country]
#     proxy.ssl_proxy = proxies[country]
#     capabilities = webdriver.DesiredCapabilities.CHROME
#     proxy.add_to_capabilities(capabilities)
#     return capabilities


# # Acessar o site por determinado país
# def test_acesso_por_pais(country, url):
#     capabilities = configure_proxy(country)
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, desired_capabilities=capabilities)
    
#     try:
#         driver.get(url)
#         print(f"Accessed {url} from {country}")
#     except Exception as e:
#         print(f"Failed to access {url} from {country}: {e}")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     url = "http://www.example.com"
#     for country in proxies.keys():
#         test_acesso_por_pais(country, url)


# # acessa o google
# driver.get("https://willian.pythonanywhere.com/views/")

# print(driver.title)
# print("Test is on!!!")
# # input_element = driver.find_element(By.CLASS_NAME, "price_button")
# # input_element.click()

# search = driver.find_element_by_name("search")

# time.sleep(100000)

# driver.quit()

# Função para simular digitação de texto
def simulate_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def test_typing_interaction():
    driver.get("https://willian.pythonanywhere.com/views")
    wait = WebDriverWait(driver, 10)
    nome_input = wait.until(EC.presence_of_element_located((By.NAME, 'nome')))
    simulate_typing(nome_input, 'willian souza')
    enviar_input = driver.find_element(By.NAME, 'enviar')
    enviar_input.click()
    time.sleep(50)
    page_content = driver.page_source
    if 'conteudo_especifico' in page_content:
        print("Página acessada com sucesso, medidas anti-scraping não detectadas.")
    else:
        print("medidas anti-scraping detectadas.")