FROM python:3.9

WORKDIR /home/sarabot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /handlers
ADD . /keyboards
ADD . main.py
ADD . .env

ENTRYPOINT ["python", "main.py"]
