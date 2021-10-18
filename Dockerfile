FROM python:3.9

WORKDIR /home/sarabot

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY .env .
#COPY handlers .
#COPY *.py ./
COPY . .