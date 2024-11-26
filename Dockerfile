FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    SECRET_KEY=django-insecure-temporary-key-for-build \
    DEBUG=False

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o projeto
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor a porta
EXPOSE 8000

# Comando para iniciar
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT