# Lista de Tarefas - Teste técnico Mayo

Esse repositório contém o código feito para realizar uma lista de tarefas com backend em Python e com um frontend feito em HTML e CSS, que realiza chamadas para a API através do AJAX (JavaScript).

## Demo 🚀

[Link da aplicação](https://todo-list-bucket.nyc3.digitaloceanspaces.com/index.html)

## Estrutura do Sistema 📁

```bash
├── backend
│   ├── .env
│   ├── Dockerfile
│   ├── auth.py
│   ├── controllers
│   │   ├── list_items_controller.py
│   │   └── users_controller.py
│   ├── db
│   │   ├── database.py
│   │   └── redis_client.py
│   ├── main.py
│   ├── models
│   │   ├── list_item.py
│   │   ├── schemas.py
│   │   └── user.py
│   ├── requirements.txt
└── frontend
    ├── index.html
    ├── script.js
    └── todo.html
```

A aplicação consiste em 2 blocos principais dividos em diretórios diferentes: o backend e o frontend. A pasta backend possui alguns arquivos auxiliares:

`requirements.txt`: Dependências necessárias para executar o backend.

`.env`: Variáveis de ambiente secretas para conexão com banco de dados (não publicado no GitHub).

`Dockerfile`: Permite a criação de uma imagem Docker para ser executada posteriormente como um container.

`auth.py`: Auxilia na autenticação dos usuários, servindo como middleware para endpoints protegidos.

O projeto segue um padrão de arquitetura MVC (Model View Controller), em que existe uma separação de tarefas no código para tratar de forma organizada os diferentes domínios do sistema. 

A pasta `models` representa as tabelas presentes no banco de dados relacional MySQL. Na aplicação, todas as transações com o banco de dados são feitas através de um ORM (Object Relational Mapping), que abstrai a lógica das queries SQL e aumenta a segurança das transações, evitando ataques como SQL Injection, por exemplo. A conexão de fato com o banco de dados se encontra dentro da pasta `db`, tanto o banco MySQL quanto o Redis.

Já a pasta `controllers` representa os comandos e queries relacionadas com os modelos do banco de dados. Todas as funções dentro dessa pasta são utilizadas dentro dos endpoints declarados dentro do arquivo `main.py`, que declara todas as rotas da aplicação e seus respectivos middlewares.

Por fim, a pasta `frontend` contém a interface gráfica do sistema feito com HTML e CSS puro. O arquivo `script.js` serve para realizar as requisições ao servidor com base nas interações do usuário com a interface.
## Tech Stack  ⚙️

**Client:** HTML, CSS, JavaScript

**Servidor:** FastAPI, Docker 

**Banco de Dados:** MySQL (dados persistentes), Redis (cache)

**Infraestrutura:** DigitalOcean AppPlatform (backend), DigitalOcean Spaces (frontend, similar ao AWS S3), DigitalOcean managed databases


## Features extra 

- Senha com hashing
- Backend conteinerizado (Docker)
- Banco de dados seguro com uso de ORM

