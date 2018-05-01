FROM python:alpine3.6
ADD code /web
WORKDIR /web
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
