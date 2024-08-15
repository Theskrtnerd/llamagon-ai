FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x init.sh
ENTRYPOINT [ "bash", "./init.sh" ]