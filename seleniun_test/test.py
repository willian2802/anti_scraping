# ------------------------ selenium ------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

#https://sites.google.com/chromium.org/driver/

# Specify the path to chromedriver.exe
# By the love of God do not change the "S" from "Service" this broken something
Service = Service(executable_path="D:/IEFP_curso/IEFP_Projects/seleniun_test/chromedriver.exe")
driver = webdriver.Chrome(service=Service)



def test_honeypot():
    try:
        # ------------------------ honeypot test ------------------------
        # Acesse a página inicial
        driver.get('https://willian.pythonanywhere.com/views')

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
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 scra (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
]

def test_agensts_detection():

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


# Executar o teste
# test_honeypot()
# test_multiple_request()
test_agensts_detection()




# # acessa o google
# driver.get("https://willian.pythonanywhere.com/views/")

# print(driver.title)
# print("Test is on!!!")
# # input_element = driver.find_element(By.CLASS_NAME, "price_button")
# # input_element.click()

# search = driver.find_element_by_name("search")

# time.sleep(100000)

# driver.quit()


