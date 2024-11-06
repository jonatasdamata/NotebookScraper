# Projeto Scraper de Notebooks - Magazine Luiza
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/jonatasdamata/NotebookScraper/blob/main/LICENSE) 

Este projeto tem como objetivo realizar a extração de dados de notebooks disponíveis no site da Magazine Luiza. O script utiliza o Selenium para navegar e extrair informações sobre os produtos, como nome, quantidade de avaliações e URLs dos itens, e organiza essas informações em um arquivo Excel.

## Funcionalidades

- **Extração de Dados:** O scraper coleta informações sobre os notebooks disponíveis no site, incluindo:
  - Nome do produto
  - Quantidade de avaliações
  - URL do produto

- **Organização de Dados:** Os dados extraídos são classificados em duas categorias:
  - **Melhores Produtos:** Notebooks com 100 ou mais avaliações.
  - **Piores Produtos:** Notebooks com menos de 100 avaliações.

- **Armazenamento:** As informações coletadas são salvas em um arquivo Excel, dividido em duas abas:
  - **Melhores:** Contém os notebooks com mais de 100 avaliações.
  - **Piores:** Contém os notebooks com menos de 100 avaliações.

- **Envio de Relatório:** Após a coleta, o script envia automaticamente o arquivo Excel por e-mail para o destinatário configurado.

## Tecnologias Utilizadas

- **Python 3.x**
- **Selenium:** Automação de navegação no navegador e extração de dados da página.
- **Pandas:** Manipulação de dados e criação de arquivos Excel.
- **Openpyxl:** Manipulação de arquivos Excel.
- **SMTP:** Envio do relatório por e-mail.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:


```mermaid
graph TD
    A[NotebookScraper] --> B[output]
    B --> C[Notebooks.xlsx]
    A --> D[logs]
    D --> E[erro_log.txt]
    A --> F[src]
    F --> G[__init__.py]
    F --> H[scrapper.py]
    A --> I[venv]
    A --> J[requirements.txt]
    A --> K[.gitignore]
````

## Requisitos

- **Python 3.x**
- **ChromeDriver** (versão compatível com a versão do seu navegador Chrome)

Para instalar as dependências do projeto, basta rodar o comando abaixo (assumindo que você tenha o Python instalado):

```bash
pip install -r requirements.txt
```

## Dependências

As dependências do projeto estão listadas no arquivo requirements.txt:

```bash
selenium
pandas
openpyxl
pyautogui
```

Para instalar as dependências, basta rodar o comando:

```bash
pip install -r requirements.txt
```

Ou se preferir, instale-as manualmente com os seguintes comandos:

```bash
pip install selenium
pip install pandas
pip install openpyxl
pip install pyautogui

```

## Como Rodar o Projeto

### 1. Baixar o ChromeDriver
Faça o download do **ChromeDriver** correspondente à versão do seu navegador Chrome.

### 2. Configurar o ChromeDriver
-Opção 1: Coloque o chromedriver.exe na mesma pasta onde está o script Python (ou dentro da pasta do projeto). <br/> <br/>
-Opção 2: Caso você prefira, você pode definir o caminho completo do chromedriver.exe diretamente no código. Para isso, altere a linha:
```bash
navegador = opcoesSelenium.Chrome()
```
Para incluir o caminho completo do ChromeDriver:
```bash
navegador = opcoesSelenium.Chrome(executable_path='C:/caminho/para/seu/chromedriver.exe')
```

### 3. Rodar o Script
Execute o script Python `scraper.py` com o comando:

```bash
python src/scraper.py
```

O script irá:

1.Acessar o site da Magazine Luiza. <br/>
2.Realizar a extração dos dados sobre notebooks.<br/>
3.Gerar um arquivo Excel contendo os dados.<br/>
4.Enviar esse arquivo por e-mail (para o e-mail configurado no código).<br/>
5.Fechar a página após a conclusão da extração e envio.

## Como Funciona o Código

### 1. Verificação do Acesso ao Site
O código começa verificando se o site está acessível, realizando até 3 tentativas de acesso ao site. Caso o site esteja fora do ar, o erro é registrado em um arquivo de log na pasta `logs/erro_log.txt`.

### 2. Extração de Dados
Após o site ser carregado com sucesso, o script pesquisa por "notebooks" na barra de pesquisa do site e aguarda até que os produtos sejam carregados.

### 3. Classificação dos Produtos
O script divide os produtos em duas listas:

- **Melhores**: Produtos com mais de 100 avaliações.
- **Piores**: Produtos com menos de 100 avaliações.

### 4. Armazenamento em Excel
As informações extraídas são salvas em um arquivo Excel, que é gerado na pasta `output/` com o nome `Notebooks.xlsx`. O arquivo possui duas abas: uma para os melhores produtos e outra para os piores.

### 5. Envio por E-mail
Após a extração e organização dos dados, o script envia automaticamente o arquivo gerado por e-mail para o endereço configurado no código.


## Logs
Se ocorrer algum erro ao acessar o site, as mensagens de erro serão registradas no arquivo `logs/erro_log.txt`.<br/>
Isso inclui informações sobre a tentativa de acessar o site e qualquer exceção gerada.


## Autor
Jonatas da Mata <br>
https://www.linkedin.com/in/jonatasdamata/



