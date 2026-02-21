
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.main:create_app()"]