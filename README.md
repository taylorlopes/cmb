![](simba/static/images/logo_labra9.png)

# CMB
Repositório do código-fonte `CMB`, uma simples aplicação Web em Python que tem por finalidade gerenciar o registro de entrada e saída de alunos fora do horário convencional do colégio.  

## Módulos
- Módulo de login
- Módulo de alunos
- Módulo de turmas
- Módulo de registros

## Tecnologias
`Python==3.11.4`\
`Flask==2.3.2`\
`Flask-SQLAlchemy==3.0.5`\
`Flask-WTF==1.1.1`\
`Jinja2==3.1.2`\
`Gunicorn==20.1.0` 
 
## Pré-requisitos
Requer instalação do [Docker](https://www.docker.com/) e do [Git](https://git-scm.com/) no servidor `Linux` que irá hospedar a aplicação.

## Instalação
Acessar via ssh o servidor `Linux` onde o Docker foi instalado <sup>[1]</sup>:
```bash
ssh root@192.168.0.1
```

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

Criar a imagem Docker (não esqueça o "." no final do comando):
```bash
docker build -t cmb:1.0 .
```

Criar o container Docker:
```
docker-compose up -d
```

Acessar a aplicação<sup>[1]</sup>:
```
https://192.168.0.1:8083/
```

Observações:\
[1] Substituir 192.168.0.1 pelo ip do servidor
 
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

Recriar o container da aplicação:
```bash
cd /var/www/cmb
docker-compose down
docker-compose up -d
```

## Banco de dados

Visualizar o tamanho do banco de dados (container):
```bash
docker exec -it cmb ls -lh db
```

Visualizar o tamanho do banco de dados (volume Docker):
```bash
ls -lh /var/lib/docker/volumes/cmb_dbdata/_data/cmb.db
```

Fazer uma cópia do banco de dados do container para o diretório corrente:
```bash
docker cp cmb:/app/db/cmb.db ./cmb.db
```

Restaurar uma cópia do banco de dados do diretório corrente para o container:
```bash
docker cp ./cmb.db cmb:/app/db/cmb.db 

docker-compose down

docker-compose up -d
```

Criar ou recriar o banco de dados da aplicação (este comando irá apagar todos os dados):
```bash
docker exec -it cmb python db-create.py --reset
```

## Senhas

Redefinir todas as senhas da aplicação (senha padrão: 12345678):
```bash
docker exec -it cmb python db-create.py --pwd
```