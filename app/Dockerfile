FROM python:3.10-slim
RUN pip install flask flask-sqlalchemy psycopg2-binary redis gunicorn
WORKDIR /app
COPY app.py .
