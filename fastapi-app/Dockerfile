FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn && \
    if [ -f pyproject.toml ]; then pip install --no-cache-dir .; fi

COPY . .

CMD ["python", "main.py"] 