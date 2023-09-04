FROM python:3.11-slim
LABEL maintainer="Copyright 2023 CMB/EB Taylor Lopes <taylor.lopes@eb.mil.br>"
RUN apt-get update
RUN apt-get install -y sqlite3 libsqlite3-dev unixodbc-dev gcc
WORKDIR /app
ENV PIP_ROOT_USER_ACTION=ignore
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY . /app
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
CMD ["python3", "db-create.py", "--reset"]
