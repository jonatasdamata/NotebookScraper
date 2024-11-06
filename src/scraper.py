import os
import smtplib
from email.message import EmailMessage
import pandas as pd
from selenium import webdriver as opcoesSelenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Função para verificar se o site foi carregado corretamente
def verificar_site():
    tentativas = 3
    url = "https://www.magazineluiza.com.br/"
    for tentativa in range(tentativas):
        try:
            # Iniciar o navegador
            navegador = opcoesSelenium.Chrome()
            navegador.get(url)
            # Esperar até que o site carregue (exemplo: verificar se o campo de pesquisa está visível)
            WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.ID, "input-search"))
            )
            print("Site carregado com sucesso!")
            return navegador  # Retorna o navegador se carregar corretamente
        except Exception as e:
            print(f"Erro ao tentar acessar o site. Tentativa {tentativa + 1} de {tentativas}.")
            if tentativa == tentativas - 1:
                # Se esgotarem as tentativas, logar o erro
                os.makedirs("logs", exist_ok=True)  # Cria a pasta logs, caso não exista
                with open("logs/erro_log.txt", "a") as log_file:
                    log_file.write(f"Site fora do ar: {time.ctime()} - Erro: {str(e)}\n")
                print("Site fora do ar. Verifique o log para mais detalhes.")
            time.sleep(2)  # Espera antes de tentar novamente
    return None  # Retorna None se não conseguir acessar o site após as tentativas

# Verificar se o site carregou corretamente
navegador = verificar_site()
if navegador is None:
    exit()  # Se não conseguir acessar o site, encerra o programa

navegador.find_element(By.ID, "input-search").send_keys("notebooks")
time.sleep(2)
navegador.find_element(By.ID, "input-search").send_keys(u'\ue007')  # Pressionar Enter

# Esperar até que os produtos estejam visíveis na página
WebDriverWait(navegador, 20).until(
    EC.visibility_of_all_elements_located((By.CLASS_NAME, "bDaikj"))
)

# Listas para armazenar dados dos produtos
listaMelhores = []
listaPiores = []

# Extrair os produtos da página
listaProdutos = navegador.find_elements(By.CLASS_NAME, "bDaikj")

for item in listaProdutos:
    nomeProduto = ""
    qtdAvaliacoes = ""
    urlProduto = ""

    try:
        nomeProduto = item.find_element(By.CLASS_NAME, "cQhIqz").text
    except Exception as e:
        print("Erro ao extrair nome:", e)

    try:
        qtdAvaliacoes = item.find_element(By.CLASS_NAME, "sc-fUkmAC").text
        if '(' in qtdAvaliacoes and ')' in qtdAvaliacoes:
            qtdAvaliacoes = qtdAvaliacoes.split('(')[-1].split(')')[0]
        else:
            qtdAvaliacoes = "0"
    except Exception as e:
        print("Erro ao extrair quantidade de avaliações:", e)

    try:
        urlProduto = item.find_element(By.TAG_NAME, "a").get_attribute("href")
    except Exception as e:
        print("Erro ao extrair URL:", e)

    if nomeProduto and qtdAvaliacoes and urlProduto:
        try:
            qtd_int = int(qtdAvaliacoes)  # Converter para inteiro
            dadosLinha = [nomeProduto, qtd_int, urlProduto]

            if qtd_int < 100:
                listaPiores.append(dadosLinha)
            else:
                listaMelhores.append(dadosLinha)

        except (ValueError, IndexError) as e:
            print(f"Erro ao processar os dados do produto: {e}")
            continue

# Verificar se existem dados para salvar
print(f"Produtos melhores: {len(listaMelhores)}")
print(f"Produtos piores: {len(listaPiores)}")

# Diretório de saída e nome do arquivo
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'Notebooks.xlsx')

# Salvando no Excel
if listaMelhores or listaPiores:
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as arquivoExcel:
        pd.DataFrame(listaMelhores, columns=['PRODUTO', 'QTD_AVAL', 'URL']).to_excel(arquivoExcel, sheet_name='Melhores', index=False)
        pd.DataFrame(listaPiores, columns=['PRODUTO', 'QTD_AVAL', 'URL']).to_excel(arquivoExcel, sheet_name='Piores', index=False)
    print("Arquivo salvo em:", output_file)
else:
    print("Nenhum dado foi extraído. Verifique os seletores e a página.")

# Função para enviar email com o relatório anexado
def enviar_email():
    email_destino = "jonatasdamatadev@gmail.com" 
    email_remetente = "jonatasdamatadev@gmail.com" 
    senha_remetente = "omsc qdke knev ergi" 
    msg = EmailMessage()
    msg['Subject'] = "Relatório Notebooks"
    msg['From'] = email_remetente
    msg['To'] = email_destino
    msg.set_content("Olá, aqui está o seu relatório dos notebooks extraídos da Magazine Luiza.\n\nAtenciosamente,\nRobô")

    with open(output_file, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='xlsx', filename="Notebooks.xlsx")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_remetente, senha_remetente)
            smtp.send_message(msg)
            print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

# Enviar o email com o arquivo
enviar_email()
