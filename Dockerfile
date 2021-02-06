FROM python:3

RUN apt-get update -y

#set envionment variables
ENV PYTHONUNBUFFERED 1

EXPOSE 5000
# RUN pip install --upgrade pip

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt


WORKDIR /app
COPY app /app

CMD python app.py
