# Define a imagem base
FROM python:3.8-slim

# Configuração do ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala o Poetry
RUN pip install poetry

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de configuração do projeto (pyproject.toml e poetry.lock)
COPY pyproject.toml poetry.lock /app/

# Instala as dependências do projeto
RUN poetry install --no-dev --no-interaction --no-ansi

# Copia o código do projeto para o diretório de trabalho
COPY . /app