FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libsqlite3-dev \
    ruby \
    ruby-dev

RUN gem install anystyle-cli

COPY requirements.txt /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt

COPY . /app

EXPOSE 8000

VOLUME /app/data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
