FROM python:3.9

WORKDIR /home

RUN apt-get update && \
    pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY .env ./
COPY bot.py ./

ENTRYPOINT ["python", "bot.py"]