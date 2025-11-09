# Alimentador

Sistema de alimentação automático para animais, integrando hardware e
software.

## 📌 Visão Geral

Este projeto apresenta o desenvolvimento de um sistema de alimentação
automática para animais, combinando **microcontrolador (C++)**,
**backend Django (Python)** e **interface web**.\
O objetivo é permitir controle, monitoramento e registro das atividades
do alimentador.

------------------------------------------------------------------------

## ⚙️ Funcionalidades

-   ✅ CRUD de agricultores cadastrados\
-   ✅ CRUD dos alimentadores (dispositivos físicos)\
-   ✅ CRUD das leituras e dados coletados\
-   ✅ Interface web simples e funcional\
-   ✅ Integração futura com o firmware do microcontrolador

------------------------------------------------------------------------

## 🧰 Tecnologias Utilizadas

### **Backend / Web**

-   Python\
-   Django\
-   SQLite\
-   HTML\
-   Bootstrap\
-   JavaScript (opcional para interações)

### **Hardware / Firmware**

-   C++\
-   Sensor ultrassônico\
-   Servo motor\
-   Microcontrolador compatível

------------------------------------------------------------------------

## 📦 Pré-requisitos

Para rodar o projeto, instale:\
- Python 3\
- Django\
- Git\
- Ambiente de compilação para o firmware em C++ (caso queira integrar)

------------------------------------------------------------------------

## 🚀 Instalação e Execução

1.  Clone o repositório:

    ``` bash
    git clone https://github.com/ErnestoSESB/Alimentador.git
    cd Alimentador
    ```

2.  Crie e ative um ambiente virtual (opcional, mas recomendado):

    ``` bash
    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    .\venv\Scripts\activate       # Windows
    ```

3.  Instale as dependências:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Crie um superusuário para acessar o admin:

    ``` bash
    python manage.py createsuperuser
    ```

5.  Execute o servidor:

    ``` bash
    python manage.py runserver
    ```

6.  Acesse no navegador:

        http://localhost:8000/

------------------------------------------------------------------------

## 🗂 Estrutura do Projeto

    Alimentador/
    ├── agricultor/      # Gerenciamento dos agricultores
    ├── alimentador/     # App principal Django
    ├── inteligente/     # Lógica futura e integrações avançadas
    ├── templates/       # Templates HTML organizados
    ├── static/          # Arquivos CSS, JS, imagens
    ├── manage.py
    ├── requirements.txt
    └── pyproject.toml   # Configurações do projeto

------------------------------------------------------------------------

## 👥 Autores

-   **Silvio Ernesto da Silva Bisneto**
-   **José Eduardo Sarmento Silva**