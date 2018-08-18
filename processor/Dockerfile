FROM python:3.6-slim

ADD code/requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

ADD code /processor
ADD nltk_data /usr/share/nltk_data
WORKDIR /processor

CMD ["python", "run.py"]