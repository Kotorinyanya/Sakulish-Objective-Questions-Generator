## QeustionBuilder

Based on [emnlp2017-relation-extraction](https://github.com/UKPLab/emnlp2017-relation-extraction) [CoreNLP](https://stanfordnlp.github.io/CoreNLP/) [sumy](https://pypi.org/project/sumy/) 

## Project structure:

|         File         |          Description           |
| :------------------: | :----------------------------: |
| relation_extraction/ | emnlp2017-relation-extraction  |
|      resources/      |      Necessary resources       |
|    trainedmodels/    | models for relation extraction |
|  NLPMainHandler.py   |        NLP main process        |
|  QuestionBuilder.py  |         Build subjects         |
|      Summer.py       |              Sumy              |
|    Paraphraser.py    |          Paraphraser           |

## Setup:

1. Check out requirements and run: </br>
    ```
    pip3 install -r requirements.txt
    ```
2. Download the [glove.6B.50d.txt](http://nlp.stanford.edu/data/glove.6B.zip) put it on `resources/embeddings/glove/glove.6B.50d.txt`
3. Download [pre-trained models](https://www.ukp.tu-darmstadt.de/fileadmin/user_upload/Group_UKP/data/wikipediaWikidata/EMNLP2017_DS_IG_relation_extraction_trained_models.zip) put it on `trainedmodels/`
4. Download [CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html) and keep it running at `localhost:9000` </br>
    ```
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
    ```
    > Note: Version of Java should be no higher than 8.
5. Install [NLTK](https://www.nltk.org/install.html)

## Requirements

- Python 3.6
- Keras 2.1.5
- TensorFLow 1.6.0

## Usage:

```
Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:14:23)
[GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from QuestionBuilder import QuestionBuilder
Using TensorFlow backend.
>>> q = QuestionBuilder(url='http://www.bbc.com/news/uk-43941624') # input could url or file or string
Loaded embeddings: (400002, 50)
Parameters: {'rnn1_layers': 1, 'bidirectional': False, 'units1': 256, 'dropout1': 0.5, 'optimizer': 'adam', 'window_size': 3, 'position_emb': 3, 'batch_size': 128, 'gpu': True, 'property2idx': 'property2idx.txt', 'wordembeddings': 'resources/embeddings/glove/glove.6B.50d.txt', 'max_sent_len': 36}
100%|###########################################| 7/7 [00:00<00:00, 2236.45it/s]
100%|###########################################| 1/1 [00:00<00:00, 3688.92it/s]
 ...
100%|###########################################| 3/3 [00:00<00:00, 3370.72it/s]
0it [00:00, ?it/s]
>>> q.subjects
{
  "RelationQuestions": [
    {
      "question": "What is the possible relationship between side door  and  car can you infer from the passage?",
      "choices": [
        "part of",
        "subclass of",
        "depicts",
        "sidekick of"
      ],
      "answer": "A"
    },
    ...
  ],
  "NerQuestions": [
    {
      "question": "The _______ slid open the side door of the car . ",
      "choices": [
        "porter",
        "shepherd",
        "River",
        "pilot"
      ],
      "answer": "A"
    },
    ...
  ],
  "TextRankQuestions": [
    {
      "question": "What is the main idea of this passage?",
      "choices": [
        "The porter slid open the side door of the car.",
        "He was so devastated that he was completely muddled by mud.",
        "He no longer likes to show off dog shows on the riverside.",
        "The dog squatted on the floor and the tail stirred the leaves."
      ],
      "answer": "A"
    }
  ],
  "CoreferenceQuestions": [
    {
      "question": "But when , followed by a group of purchasing sportsmen , the widow came to the kennel where he waited at the end of <u>his</u>_<u>chain</u> , she had clasped her hands together and cried out : `` I wo n't sell this one ! '' \nWhat does the underline word \"his chain\" mention in this sentence?",
      "choices": [
        "the taut chain",
        "his tail",
        "their",
        "The Jersey kennels of George Devant"
      ],
      "answer": "A"
    },
    ...
  ]
}
```
