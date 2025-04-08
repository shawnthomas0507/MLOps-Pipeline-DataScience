FROM python:3.10-alpine

WORDKDIR /app
COPY . /app 

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt

EXPOSE 5000

CMD ["python3","app.py"]

