FROM java:openjdk-8-jre-alpine

ADD code /core
WORKDIR /core

CMD ["java", "-mx8g", "-cp", "*", "edu.stanford.nlp.pipeline.StanfordCoreNLPServer", "-timeout", "60000"]
