Este projeto visa apresentar de forma visual um projeto desenvolvido por meio de código livre - a implementação de um sistema de alimentação automático para animais. Este software foi desenvolvido em C++ e faz a utilização de um sonar, um servo-motor e outros periféricos, já a linguagem utilizada na parte web é python.

DESENVOLVEDORES: Silvio Ernesto da Silva Bisneto, José Eduardo Sarmento Silva

Recursos ultilizados:

Django 4.2.2

Python 3.0

SQlite

HTML/CSS/Bootstrap

Funcionalidades:

- CRUD de agricultores interessados


- CRUD de dados coletados do alimentador


- CRUD de dados sobre o alimentador
Pré-requisitos:

Faça a instalação do Python em seu sistema operacional através de: https://www.python.org/downloads/

Faça a instalação do Django em seu sistema operacional através de: https://www.djangoproject.com/download/

Instruções de Execução:

Clone o repositório com o comando: git clone https://github.com/ErnestoSESB/Intelligent_feeder.git

Instale o ambiente virtual: python -m venv venv .

Rode o ambiente virtual: .\Venv\Scripts\activate

Instale as dependências com o comando: pip install -r requeriments.txt

Crie um superusuario: python manage.py createsuperuser

Rode o servidor com o comando python manage.py runserver

Acesse o sistema em http://localhost:8000
