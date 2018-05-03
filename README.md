# BaiduAIProject

To generate English objective questions from English materials with neural networks.

## Project Document

[https://hackmd.io/D9C-gD16Q6yTx8PrQBR3Og](https://hackmd.io/D9C-gD16Q6yTx8PrQBR3Og)

## How to Run It with Docker

!!! WARNING: docker of text_processor is BROKEN so far !!!

!!! Skip this section please !!!

1. Install Docker and Docker Compose.

2. Prepare the environment as `README.md` in `text_processor/code` folder, so that you can run it dependently as described in readme.

3. Extra, download JRE 8u172 at [this page](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html), and put it in `text_processor/code/java`.

4. Now, in `text_processor/code` folder you should be able to run NLP server with `java/bin/java -mx4g -cp "stanford-corenlp-full-2018-02-27/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer`.

5. In this folder, run `docker-compose up` as `root`.

After building & downloading images, the docker containers should be running.

The steps will be much simpler when we use PaddlePaddle.

Web GUI: [http://127.0.0.1:10086](http://127.0.0.1:10086)

## How to Run Them without Docker Compose

1. Run a Redis docker and map its port 6379 out.

2. Run text processor with `python3 run.py --host <Redis Server IP> --port <Redis Port>`.

3. Run web server with `python3 app.py --host <Redis Server IP> --port <Redis Port>`.

 > You can get rid of docker completely by installing Redis somewhere instead of using Redis docker container.

Web GUI: `http://<Web Server IP>:10086`