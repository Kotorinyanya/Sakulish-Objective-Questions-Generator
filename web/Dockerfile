FROM python:alpine3.6

ADD code/requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

ADD code /web
WORKDIR /web

CMD ["python", "app.py"]
