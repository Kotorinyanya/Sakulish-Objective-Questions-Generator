# Sakulish Objective Questions Generator

To generate English objective questions from English materials with neural networks.

Sakulish 就是 English 的意思，因为 Sakura 是樱花，Sakulish 就是嘤语

## Preview

![home](http://ww1.sinaimg.cn/large/006tNc79gy1g4lkrc87a6j30j60hm75e.jpg)
![questions](http://ww2.sinaimg.cn/large/006tNc79gy1g4lkro5cp3j30j60hm75y.jpg)

## Project Document

[https://hackmd.io/s/S1hFM3ZAM](https://hackmd.io/s/S1hFM3ZAM)

## Preparation

Since some models and dependencies are too large in size, you have to download it additionally.

[Download from Google Driver](https://drive.google.com/open?id=1gyK5abr3VGS2FKxwASMcTGd6t4VQn6BX)

All four zip files are needed. After unzipping, please place the unzipped files as following:

- File `glove.6B.50d.txt` from `glove.zip` : `processor/code/resources/embeddings/glove/glove.6B.50d.txt`
- Folder `trainedmodels` from `trainedmodels.zip` : `processor/code/trainedmodels`
- Folder `nltk_data` from `nltk_data.zip` : `processor/nltk_data`
- Folder `code` from `corenlp.zip` : `corenlp/code`

## Run with Docker Compose

1. Install Docker and Docker Compose.
2. Prepare the environment as the `Preparation` section above.
3. Run `docker-compose up` and wait for building.
4. Now it's running.

Web GUI: [http://127.0.0.1:10086](http://127.0.0.1:10086)
