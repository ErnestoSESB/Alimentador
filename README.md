# SmartFeeder Auto

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

-   ✅ CRUD de agricultores cadastrados;
-   ✅ CRUD dos alimentadores (dispositivos físicos);
-   ✅ CRUD das leituras e dados coletados;
-   ✅ Interface web simples e funcional;
-   ✅ Integração futura com o firmware do microcontrolador;

------------------------------------------------------------------------

## 🧰 Tecnologias Utilizadas

### **Backend / Web**

-   Python;
-   Django;
-   SQLite;
-   HTML;
-   Bootstrap;
-   JavaScript (opcional para interações);

### **Hardware / Firmware**

-   C++;
-   Sensor ultrassônico;
-   Servo motor;
-   Microcontrolador compatível;

------------------------------------------------------------------------

## 📦 Pré-requisitos

Para rodar o projeto, instale:
- Python 3;
- Django;
- Git;
- Ambiente de compilação para o firmware em C++ (caso queira integrar);

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

## 🖼 Imagens do Sistema 

## !!⚠ ATENÇÃO ⚠!!
As imagens contidas abaixo representam a visão do administrador, as imagens não representam dados reais de usuarios, são apenas dados simulados através de algoritmos e inserções manuais quaisquer dados apresentado pelo meio visual disponibilizado são inexistentes das aplicações reais do projeto. As imagens também não representam a totalidade das abas do projeto e não dispensam a necessidade da instalação do ambiente virtual para ver a totalidade do sistema.

Dashboard:
<img width="1976" height="926" alt="SmartFeeder-Dashboard" src="https://github.com/user-attachments/assets/32569ea2-3228-4ce5-833f-edd5c876cf1d" />

Alimentadores:
<img width="1920" height="925" alt="SmartFeeder-Alimentadores" src="https://github.com/user-attachments/assets/989245b8-e70c-4f03-960f-749eda24839b" />

Usuarios:
<img width="1919" height="930" alt="SmartFeeder-Usuarios" src="https://github.com/user-attachments/assets/01b38879-b6a2-4968-a381-36c88bf95f68" />

Alertas:
<img width="1919" height="924" alt="SmartFeeder-Alerts" src="https://github.com/user-attachments/assets/df71f351-ac79-47b2-8a31-1fccbd7146a8" />

Relatórios:
<img width="1917" height="927" alt="SmartFeeder-Relatorios" src="https://github.com/user-attachments/assets/674b81e9-fea9-4494-9dcc-b24069d1ddd3" />


## 👥 Autores

-   **Silvio Ernesto da Silva Bisneto**
-   **José Eduardo Sarmento Silva**
