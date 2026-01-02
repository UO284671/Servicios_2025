FROM python:3.9
WORKDIR /amigos
RUN pip install --no-cache-dir flask flask-sqlalchemy pymysql cryptography firebase-admin gunicorn flask-migrate
COPY . /amigos
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app('development')"]