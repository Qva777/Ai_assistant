FROM python:3.11


RUN mkdir /app
WORKDIR /app

RUN apt update

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5001

RUN chmod +x ./start.sh
CMD ["/bin/bash", "./start.sh"]

