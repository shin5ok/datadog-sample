FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh -o /tmp/uv-install.sh && \
    sh /tmp/uv-install.sh && \
    mv $HOME/.local/bin/uv /usr/local/bin/uv && \
    uv sync

COPY . .

CMD ["uv", "run", "main.py"] 