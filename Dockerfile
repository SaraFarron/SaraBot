FROM python:3.9

WORKDIR /home

RUN apt-get update && apt-get install sqlite3 && \
    pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY .env ./
COPY bot.py ./
COPY *.sqlite ./
RUN sqlite3 dictionary.db < create.db

ENTRYPOINT ["python", "bot.py"]