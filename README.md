![](simba/static/images/logo_labra9.png)

# CMB
Repositório do código-fonte `CMB`, uma simples aplicação Web que tem por finalidade gerenciar o registro de entrada e saída de alunos fora do horário convencional do colégio.  

## Módulos
- Módulo de login
- Módulo de alunos
- Módulo de turmas
- Módulo de registros (entrada/saída)

## Tecnologias

### Backend
`Docker v20.10.5`\
`Python==3.11.4`\
`Flask==2.3.2`\
`Flask-SQLAlchemy==3.0.5`\
`Flask-WTF==1.1.1`\
`Jinja2==3.1.2`\
`Gunicorn==20.1.0` 

### Frontend
`Bootstrap  v5.3.0`\
`Font Awesome Free v6.4.0`\
`jQuery v3.6.3`\
`DataTables v1.13.6`\
`Moment.js v2.18.1`\
`Ajax Autocomplete for jQuery v1.4.11`\
`Daterangepicker v3.1.0`


## Pré-requisitos
Requer instalação prévia do [Docker](https://www.docker.com/) e do [Git](https://git-scm.com/) no servidor que irá hospedar a aplicação. Utilize preferencialmente `Linux` [Debian](https://www.debian.org/) ou derivados.

Instalar o docker e docker-compose:
```bash
wget https://raw.githubusercontent.com/taylorlopes/docker/main/docker-install.sh

chmod +x docker-install.sh

./docker-install.sh
```

Instalar o git:
```bash
sudo apt-get update

sudo apt-get install git
```

## Instalação

Acessar o diretório de publicação:
```bash
cd /var/www
```

Baixar o código-fonte do repositório git:
```bash
git clone https://github.com/taylorlopes/cmb.git
```

Acessar o diretório da aplicação:
```bash
cd /var/www/cmb
```

Criar a imagem docker (não esqueça o "." no final do comando):
```bash
docker build -t cmb:1.0 .
```

Criar o container Docker:
```
docker-compose up -d
```

Acessar a aplicação (substituir 192.168.0.1 pelo ip do servidor, senha padrão: 12345678):
```
https://192.168.0.1:8083/
```

Observações:\
[1] Trocar a chave SECRET_KEY, em [.env](https://github.com/taylorlopes/cmb/blob/main/.env)\
[2] Gerar novos arquivos auto-assinado PEM, em [ssl](https://github.com/taylorlopes/cmb/tree/main/ssl)

 
## Atualização

Acessar o diretório da aplicação:
```bash
cd /var/www/cmb
```

Atualizar o código-fonte:
```bash
git pull origin main
```

## Container

Acessar o container da aplicação:
```bash
docker exec -it cmb /bin/bash
```

Criar ou recriar o container da aplicação:
```bash
cd /var/www/cmb

docker-compose down

docker-compose up -d
```

## Banco de dados

> O docker localmente cria um volume com os dados em `/var/lib/docker/volumes/cmb_dbdata/_data/cmb.db`

Visualizar o tamanho do banco de dados:
```bash
docker exec -it cmb ls -lh db
```

Fazer uma cópia do banco de dados do container para o diretório corrente:
```bash
docker cp cmb:/app/db/cmb.db ./cmb.db
```

Restaurar uma cópia do banco de dados do diretório corrente para o container:
```bash
docker cp ./cmb.db cmb:/app/db/cmb.db 

cd /var/www/cmb

docker-compose down

docker-compose up -d
```

Criar ou recriar o banco de dados da aplicação. ATENÇÃO: este comando irá apagar todos os dados:
```bash
docker exec -it cmb python db-create.py --reset
```

## Senhas

Redefinir todas as senhas da aplicação (senha padrão: 12345678):
```bash
docker exec -it cmb python db-create.py --pwd
```
