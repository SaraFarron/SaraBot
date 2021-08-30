FROM python:3.9

WORKDIR /home/SaraBot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python", "app.py"]
