

Descrição do Projeto
Este projeto implementa um sistema de segurança para proteger aplicações web contra acessos não autorizados, requisições excessivas, e outras atividades suspeitas. O sistema realiza uma série de verificações em cada requisição, identificando possíveis ameaças e tomando medidas preventivas para garantir a segurança da aplicação.

Funcionamento:

Coleta de Dados:

Cada requisição coleta informações do usuário, como endereço IP, agente do usuário (User-Agent), e um fingerprint gerado com base nas características do dispositivo e sistema operacional.
Isso gera um log com essas informaçoes que é armazenado no MongoDB, junto com a criaçao de um perfil chamda IP_data que tem todos os dados sobre aquele IP especifico fingerprint, quantidade de requisiçoes, ultimo_acesso, localiade, etc..., isso ajuda a ter um melhor monitoramento e checagem de atividades suspeitas. 
Verificações de Segurança:

IP Anônimo e Proxy: O sistema pode identificar e bloquear IPs que utilizam VPNs ou proxies anônimos.
Localização Geográfica: A localização do IP é verificada, bloqueando acessos de países não autorizados.
Controle de Requisições: Limita o número de requisições permitidas em um curto período de tempo e o total de requisições de um IP específico.
Agentes de Usuário Suspeitos: Bloqueia requisições de agentes que indicam bots, scrapers ou navegadores headless.
Bloquei os usuarios de acordo com listas: varias litas como IP_black_list, Country_black_list entre outras listas que estao armazenadas no MongoDB sao usadas para barar o acesso.

Logs e Auditoria:

Cada requisição gera um log que é armazenado no MongoDB junto com o IP_data, permitindo auditoria e análise de atividades suspeitas com uma eficiencia muito maior.
Respostas Automáticas:

Dependendo das verificações, o sistema pode bloquear o acesso, ativar um modo de redução de velocidade (slow_down), ou permitir o acesso normalmente.
Benefícios:
Este sistema é ideal para proteger aplicativos web contra ataques automatizados, minimizar o impacto de bots, e garantir que o acesso seja feito apenas por usuários legítimos. Além disso, ele fornece uma camada adicional de segurança baseada em geolocalização e características do dispositivo, garantindo maior controle sobre quem pode acessar sua aplicação.
Link:https://willian.pythonanywhere.com/views/
