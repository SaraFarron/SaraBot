FROM python:3.9

RUN pip install --upgrade pip

COPY . ./
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]
