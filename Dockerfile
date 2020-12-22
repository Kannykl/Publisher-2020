FROM python:3.9-slim
WORKDIR /home/kanny

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install netcat -y
RUN pip install --upgrade pip

COPY requirements.txt /home/kanny/requirements.txt
RUN pip install -r requirements.txt

COPY . /home/kanny

ENTRYPOINT ["/home/kanny/entrypoint.sh"]
